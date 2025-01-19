from django.urls import path
from .views import CampaignListCreateView, SyncCampaignDataView

urlpatterns = [
    path('', CampaignListCreateView.as_view(), name='campaign-list-create'),  # عرض إنشاء وعرض الحملات
    path('<int:campaign_id>/sync/', SyncCampaignDataView.as_view(), name='campaign-sync'),  # مزامنة البيانات
]
