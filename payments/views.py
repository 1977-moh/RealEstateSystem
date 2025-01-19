from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from django.core.paginator import Paginator


class PaymentListCreateView(APIView):
    """
    عرض لإنشاء واستعراض المدفوعات.
    """

    def get(self, request):
        """
        استرجاع قائمة المدفوعات مع دعم التصفية.
        """
        # جلب جميع المدفوعات
        payments = Payment.objects.all()

        # تصفية البيانات بناءً على معلمات الطلب (اختياري)
        method = request.query_params.get('method')  # التصفية حسب طريقة الدفع
        date = request.query_params.get('date')  # التصفية حسب التاريخ
        if method:
            payments = payments.filter(method=method)
        if date:
            payments = payments.filter(date=date)

        # دعم التصفح (pagination)
        paginator = Paginator(payments, 10)  # عرض 10 عناصر لكل صفحة
        page = request.query_params.get('page', 1)
        payments_page = paginator.get_page(page)

        # تسلسل البيانات وإرجاعها
        serializer = PaymentSerializer(payments_page, many=True)
        return Response({
            "total": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": int(page),
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        إنشاء دفعة جديدة.
        """
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
