import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Campaign
from .serializers import CampaignSerializer
from leads.tasks import distribute_leads
from leads.models import Lead

# ✅ إعداد سجل الأخطاء لتسجيل المشاكل
logger = logging.getLogger(__name__)


class CampaignListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض جميع الحملات وإنشاء حملة جديدة
    """
    queryset = Campaign.objects.all().order_by('-created_at')
    serializer_class = CampaignSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['platform', 'status', 'start_date', 'end_date']
    search_fields = ['name', 'platform']
    ordering_fields = ['created_at', 'budget', 'start_date', 'end_date']


class CampaignDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تحديث أو حذف حملة معينة
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        """
        ✅ السماح فقط للمستخدمين الإداريين بحذف الحملات.
        """
        if not self.request.user.is_staff:
            logger.warning(f"⚠️ User {self.request.user} attempted to delete a campaign without permission.")
            return Response(
                {"error": "🚫 You do not have permission to delete campaigns."},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
        return Response({"message": "✅ Campaign deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class SyncCampaignDataView(APIView):
    """
    ✅ مزامنة بيانات الحملة مع API خارجي وتحميل العملاء المحتملين (Leads)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)

        if not campaign.campaign_url:
            logger.error(f"❌ Campaign {campaign.id} has no URL for synchronization.")
            return Response({"error": "❌ Campaign URL is not set."}, status=status.HTTP_400_BAD_REQUEST)

        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
        session.mount('https://', HTTPAdapter(max_retries=retries))

        headers = {
            "User-Agent": "RealEstateCRM/1.0",
            "Accept": "application/json",
        }

        try:
            response = session.get(campaign.campaign_url, timeout=10, headers=headers)

            if response.status_code != 200:
                logger.error(f"❌ API returned status {response.status_code} for campaign {campaign.id}.")
                return Response({"error": f"❌ Failed to fetch campaign data (Status {response.status_code})."},
                                status=status.HTTP_502_BAD_GATEWAY)

            campaign_data = response.json()
            failed_leads = []
            success_count = 0

            for lead in campaign_data.get("leads", []):
                if not lead.get("email") or not lead.get("name"):
                    failed_leads.append({"lead": lead, "error": "Missing required fields"})
                    continue

                try:
                    _, created = Lead.objects.get_or_create(
                        campaign=campaign,
                        name=lead.get("name"),
                        email=lead.get("email"),
                        phone=lead.get("phone"),
                    )
                    if created:
                        success_count += 1

                except Exception as e:
                    logger.error(f"❌ Failed to save lead: {str(e)}")
                    failed_leads.append({"lead": lead, "error": str(e)})

            distribute_leads.apply_async()

            response_data = {
                "message": "✅ Campaign data synchronized successfully.",
                "leads_imported": success_count,
            }

            if failed_leads:
                response_data["warning"] = "⚠️ Some leads failed to import."
                response_data["failed_leads"] = failed_leads
                return Response(response_data, status=status.HTTP_206_PARTIAL_CONTENT)

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            logger.critical(f"❌ Request failed for campaign {campaign.id}: {str(e)}")
            return Response({"error": f"❌ Failed to fetch campaign data: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CampaignPerformanceReportView(APIView):
    """
    ✅ توليد تقرير أداء الحملة بما في ذلك `ROI, Budget Efficiency, Lead Conversion Rate`
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)
        report = campaign.generate_report()

        return Response({
            "message": "📊 Campaign Performance Report",
            "data": report
        }, status=status.HTTP_200_OK)


class PauseResumeCampaignView(APIView):
    """
    ✅ إيقاف أو استئناف الحملة بناءً على أداء `ROI`
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        campaign = get_object_or_404(Campaign, id=pk)

        if campaign.calculate_roi < 10:
            campaign.status = "Paused"
            campaign.save()
            return Response({"message": "🚨 Campaign paused due to low ROI."}, status=status.HTTP_200_OK)

        elif campaign.calculate_roi > 50:
            campaign.status = "Active"
            campaign.save()
            return Response({"message": "✅ Campaign resumed due to high performance!"}, status=status.HTTP_200_OK)

        return Response({"message": "ℹ️ No changes needed."}, status=status.HTTP_200_OK)
