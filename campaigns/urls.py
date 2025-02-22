from django.urls import path
from .views import (
    CampaignListCreateView,
    CampaignDetailView,
    SyncCampaignDataView,
    CampaignPerformanceReportView,
    PauseResumeCampaignView
)

# ✅ تعيين اسم التطبيق لتسهيل استدعاء المسارات في أماكن أخرى
app_name = 'campaigns'

urlpatterns = [
    path('', CampaignListCreateView.as_view(), name='campaign-list-create'),  # ✅ عرض وإنشاء الحملات
    path('<uuid:pk>/', CampaignDetailView.as_view(), name='campaign-detail'),  # ✅ عرض/تحديث/حذف حملة معينة
    path('<uuid:pk>/sync/', SyncCampaignDataView.as_view(), name='campaign-sync'),  # ✅ مزامنة بيانات الحملة
    path('<uuid:pk>/report/', CampaignPerformanceReportView.as_view(), name='campaign-report'),  # ✅ تقرير أداء الحملة
    path('<uuid:pk>/pause-resume/', PauseResumeCampaignView.as_view(), name='campaign-pause-resume'),  # ✅ إيقاف/استئناف الحملات
]
