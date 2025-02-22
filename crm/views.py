from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from .models import Client, Lead, ClientActivity, AIRecommendation
from .serializers import (
    ClientSerializer, LeadSerializer, ClientActivitySerializer, AIRecommendationSerializer
)
from .web_scraper import fetch_potential_clients


class ClientListView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة العملاء أو إنشاء عميل جديد.
    📊 يدعم البحث الذكي والفلاتر.
    """
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'email', 'phone', 'client_source']
    ordering_fields = ['created_at', 'updated_at', 'status']
    filterset_fields = ['status', 'assigned_employee', 'client_source']


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ إدارة تفاصيل العميل (عرض/تحديث/حذف).
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]


class LeadListView(generics.ListCreateAPIView):
    """
    ✅ إدارة العملاء المحتملين مع دعم البحث.
    🔍 يمكن البحث حسب اسم العميل أو الحملة.
    """
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['client__name', 'campaign__name']
    filterset_fields = ['campaign', 'interest_level']


class ClientActivityView(generics.ListCreateAPIView):
    """
    ✅ إدارة سجلات الأنشطة والتفاعلات مع العميل.
    """
    queryset = ClientActivity.objects.all().order_by('-timestamp')
    serializer_class = ClientActivitySerializer
    permission_classes = [IsAuthenticated]


class AIRecommendationView(generics.ListAPIView):
    """
    ✅ عرض توصيات الذكاء الصناعي بناءً على بيانات العملاء.
    🧠 يحدد أفضل العروض وفقًا لتحليل العميل.
    """
    queryset = AIRecommendation.objects.all().order_by('-generated_at')
    serializer_class = AIRecommendationSerializer
    permission_classes = [IsAuthenticated]


class SocialMediaLeadImportView(generics.ListCreateAPIView):
    """
    ✅ استيراد العملاء المحتملين تلقائيًا من Google, Instagram, TikTok.
    """
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        📡 تشغيل البحث الذكي عن العملاء المحتملين.
        """
        return fetch_potential_clients()
