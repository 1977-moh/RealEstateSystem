from rest_framework import generics, filters, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Payment
from .serializers import PaymentSerializer


class CustomPagination(PageNumberPagination):
    """
    ✅ إعداد التصفح (Pagination) لتحديد عدد العناصر في كل صفحة.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaymentListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض لإنشاء واستعراض المدفوعات مع ميزات محسّنة:
    - البحث المتقدم
    - التصفية حسب عدة معايير
    - التصفح (pagination)
    - الفرز
    """
    serializer_class = PaymentSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    # ✅ دعم البحث والفرز
    search_fields = ['method', 'description', 'amount', 'date']
    ordering_fields = ['amount', 'date', 'method']
    ordering = ['-date', '-created_at']  # ✅ الترتيب الافتراضي من الأحدث إلى الأقدم

    def get_queryset(self):
        """
        ✅ تطبيق التصفية الديناميكية عند استرجاع المدفوعات.
        """
        queryset = Payment.objects.all()
        request = self.request

        filters = Q()
        if (method := request.query_params.get('method')):
            filters &= Q(method__icontains=method)
        if (date := request.query_params.get('date')):
            filters &= Q(date=date)
        if (min_amount := request.query_params.get('min_amount')):
            filters &= Q(amount__gte=min_amount)
        if (max_amount := request.query_params.get('max_amount')):
            filters &= Q(amount__lte=max_amount)
        if (search := request.query_params.get('search')):
            filters &= Q(description__icontains=search) | Q(method__icontains=search) | Q(amount__icontains=search)

        return queryset.filter(filters)

    def post(self, request, *args, **kwargs):
        """
        ✅ إنشاء دفعة جديدة مع التحقق من صحة البيانات ومنع التكرار.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            method = serializer.validated_data['method']
            date = serializer.validated_data['date']

            # التحقق مما إذا كانت هناك دفعة مشابهة خلال آخر 5 دقائق
            if Payment.objects.filter(amount=amount, method=method, date=date).exists():
                return Response({
                    "error": "🚨 هذه الدفعة مسجلة بالفعل!",
                    "payment": serializer.data
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                "message": "✅ تم إنشاء الدفعة بنجاح!",
                "payment": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "error": "🚨 حدث خطأ في البيانات.",
            "details": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض / تعديل / حذف دفعة محددة
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_update(self, serializer):
        """
        ✅ منع تعديل `date` بعد إنشاء الدفعة.
        """
        serializer.validated_data.pop('date', None)
        serializer.save()
