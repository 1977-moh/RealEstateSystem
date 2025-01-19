from django.urls import path
from .views import LeadListCreateView

app_name = 'leads'  # إضافة اسم التطبيق لتجنب التضارب في الأسماء في المشروع

urlpatterns = [
    path('', LeadListCreateView.as_view(), name='list-create'),  # ربط العرض الأساسي
]
