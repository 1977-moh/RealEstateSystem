from django.urls import path
from .views import LeadListCreateView, LeadDetailView

app_name = 'leads'  # ✅ تعريف اسم التطبيق لمنع التضارب

urlpatterns = [
    path('', LeadListCreateView.as_view(), name='lead-list-create'),  # ✅ عرض جميع Leads وإنشاء جديد
    path('<uuid:pk>/', LeadDetailView.as_view(), name='lead-detail'),  # ✅ عرض/تحديث/حذف Lead معين
]
