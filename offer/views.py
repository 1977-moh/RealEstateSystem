from rest_framework import generics, filters, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Offer
from .serializers import OfferSerializer


class OfferPagination(PageNumberPagination):
    """
    ✅ إعداد التصفح بحيث يكون عدد العروض في الصفحة 10.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class OfferListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة العروض أو إنشاء عرض جديد.
    - دعم التصفح (pagination).
    - دعم البحث والتصفية.
    - دعم الترتيب حسب التاريخ.
    """
    queryset = Offer.objects.all().order_by('-created_at')  # ✅ ترتيب حسب الأحدث
    serializer_class = OfferSerializer
    pagination_class = OfferPagination
    permission_classes = [permissions.IsAuthenticated]  # ✅ السماح فقط للمستخدمين المصادق عليهم

    # ✅ دعم البحث والفلترة والترتيب
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']  # ✅ البحث حسب العنوان والوصف
    filterset_fields = ['status', 'offer_type', 'assigned_employee']  # ✅ تصفية حسب الحالة ونوع العرض والموظف
    ordering_fields = ['start_date', 'end_date', 'created_at']  # ✅ ترتيب حسب التواريخ

    def perform_create(self, serializer):
        """
        ✅ تعيين المستخدم الحالي كالموظف المسؤول عن العرض، إذا لم يتم تعيينه.
        """
        if not serializer.validated_data.get('assigned_employee'):
            serializer.save(assigned_employee=self.request.user)
        else:
            serializer.save()


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تحديث، أو حذف عرض معين.
    - السماح فقط للمستخدمين المصادق عليهم.
    - السماح للمسؤولين فقط بحذف العرض.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        """
        ✅ منع حذف العروض النشطة.
        """
        if instance.status == "Active":
            raise permissions.PermissionDenied("🚨 Active offers cannot be deleted.")

        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("🚨 Only admins can delete offers.")

        instance.delete()


class OfferActivateView(APIView):
    """
    ✅ تفعيل أو تعطيل العرض.
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        offer = generics.get_object_or_404(Offer, pk=pk)
        offer.is_active = not offer.is_active
        offer.save()
        return Response({"message": f"Offer {'activated' if offer.is_active else 'deactivated'} successfully."},
                        status=status.HTTP_200_OK)
