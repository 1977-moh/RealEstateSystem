from django.urls import path
from .views import ClientListView, ClientDetailView

# Namespace للتطبيق
app_name = 'clients'

# تعريف المسارات
urlpatterns = [
    path('', ClientListView.as_view(), name='client-list'),  # عرض قائمة العملاء أو إضافة عميل جديد
    path('<int:pk>/', ClientDetailView.as_view(), name='client-detail'),  # عرض/تحديث/حذف عميل معين
]
