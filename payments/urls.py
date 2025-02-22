from django.urls import path
from .views import PaymentListCreateView, PaymentDetailView

# ✅ تعريف مساحة أسماء للتطبيق لمنع التضارب
app_name = 'payments'

urlpatterns = [
    path('', PaymentListCreateView.as_view(), name='payment-list-create'),  # ✅ إدارة جميع المدفوعات
    path('<uuid:pk>/', PaymentDetailView.as_view(), name='payment-detail'),  # ✅ عرض / تعديل / حذف دفعة معينة
]
