from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Campaign
from .serializers import CampaignSerializer
from leads.tasks import distribute_leads
from leads.models import Lead
import requests


class CampaignListCreateView(APIView):
    def get(self, request):
        """عرض جميع الحملات."""
        campaigns = Campaign.objects.all()
        serializer = CampaignSerializer(campaigns, many=True)
        return Response(serializer.data)

    def post(self, request):
        """إنشاء حملة جديدة."""
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SyncCampaignDataView(APIView):
    def get(self, request, campaign_id):
        """مزامنة بيانات الحملة."""
        # الحصول على الحملة أو عرض خطأ 404 إذا لم يتم العثور عليها
        campaign = get_object_or_404(Campaign, id=campaign_id)

        if not campaign.campaign_url:
            return Response({"error": "Campaign URL is not set."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # استدعاء API المزامنة
            response = requests.get(campaign.campaign_url, timeout=10)
            response.raise_for_status()  # التحقق من أي خطأ HTTP

            campaign_data = response.json()

            # حفظ الليدز المأخوذة من الـ API
            for lead in campaign_data.get("leads", []):
                Lead.objects.get_or_create(  # التأكد من عدم تكرار الليدز
                    campaign=campaign,
                    name=lead.get("name"),
                    email=lead.get("email"),
                    phone=lead.get("phone"),
                )

            # توزيع الليدز بعد استيرادها
            distribute_leads()
            return Response({"success": "Campaign data synchronized and leads distributed successfully."})

        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to fetch campaign data: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
