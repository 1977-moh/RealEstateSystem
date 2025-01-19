from django.urls import path
from .views import PaymentListCreateView

# تعريف مساحة أسماء للتطبيق
app_name = 'payments'

urlpatterns = [
    # عرض قائمة المدفوعات وإنشاء دفعة جديدة
    path('', PaymentListCreateView.as_view(), name='list-create'),
]
