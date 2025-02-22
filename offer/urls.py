from django.urls import path
from .views import OfferListCreateView, OfferDetailView, OfferActivateView

# ✅ تعريف مساحة أسماء التطبيق
app_name = 'offers'

urlpatterns = [
    path('', OfferListCreateView.as_view(), name='offer-list'),  # ✅ عرض جميع العروض أو إضافة عرض جديد
    path('<uuid:pk>/', OfferDetailView.as_view(), name='offer-detail'),  # ✅ عرض/تحديث/حذف عرض معين
    path('<uuid:pk>/activate/', OfferActivateView.as_view(), name='offer-activate'),  # ✅ تفعيل أو تعطيل العرض
]
