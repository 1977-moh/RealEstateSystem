from django.urls import path
from .views import PropertyListView, PropertyDetailView

# ✅ تحديد `app_name` لمنع التضارب في المشروع
app_name = 'properties'

urlpatterns = [
    # ✅ عرض قائمة العقارات وإمكانية إنشاء عقار جديد
    path('', PropertyListView.as_view(), name='property-list'),

    # ✅ عرض/تحديث/حذف عقار محدد بناءً على `UUID`
    path('<uuid:pk>/', PropertyDetailView.as_view(), name='property-detail'),
]
