from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend  # ✅ استيراد صحيح لـ `DjangoFilterBackend`
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.apps import apps  # ✅ تجنب الاستيراد الدائري
from .models import Broker, BrokerClient, BrokerTransaction
from .serializers import (
    BrokerSerializer, BrokerClientSerializer, BrokerTransactionSerializer, EmployeePerformanceSerializer
)

# ✅ جلب `EmployeePerformance` فقط عند الحاجة لتجنب الاستيراد الدائري
EmployeePerformance = apps.get_model("employees", "EmployeePerformance")


# === 🔹 إعداد التصفح (Pagination) ===
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


# === 🔹 مزيج مشترك لكل الـ Views لإعادة استخدام الإعدادات ===
class BaseListView(generics.ListCreateAPIView):
    """
    ✅ هذا الـ View يعالج عمليات `GET` و `POST` للعناصر مع دعم التصفح والترتيب والبحث.
    """
    pagination_class = CustomPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]  # ✅ تصحيح الخطأ


class BaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ هذا الـ View يعالج `GET` و `PUT` و `DELETE` بناءً على `id` مع التحقق من الصلاحيات.
    """
    lookup_field = "id"

    def get_permissions(self):
        """
        ✅ يسمح للجميع بالوصول، لكن يطلب إذن المشرف فقط للحذف.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]


# === 🏢 إدارة الوسطاء (Brokers) ===
class BrokerListCreateView(BaseListView):
    """
    ✅ إنشاء وعرض قائمة الوسطاء مع دعم البحث والترتيب والتصفية.
    """
    queryset = Broker.objects.all().order_by('-created_at')
    serializer_class = BrokerSerializer
    search_fields = ['name', 'email', 'contact_number']
    ordering_fields = ['name', 'created_at']
    filterset_fields = ['responsible_employee', 'commission_rate']


class BrokerDetailView(BaseDetailView):
    """
    ✅ عرض وتحديث وحذف وسيط محدد.
    """
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer


# === 👥 إدارة العلاقات بين الوسطاء والعملاء (Broker-Client Relations) ===
class BrokerClientListCreateView(BaseListView):
    """
    ✅ إنشاء وعرض قائمة العلاقات بين الوسطاء والعملاء مع دعم البحث والترتيب والتصفية.
    """
    queryset = BrokerClient.objects.all().order_by('-created_at')
    serializer_class = BrokerClientSerializer
    search_fields = ['broker__name', 'client__name']
    ordering_fields = ['created_at', 'commission_amount']
    filterset_fields = ['broker', 'client', 'status']


class BrokerClientDetailView(BaseDetailView):
    """
    ✅ عرض وتحديث وحذف علاقة معينة بين وسيط وعميل.
    """
    queryset = BrokerClient.objects.all()
    serializer_class = BrokerClientSerializer


# === 💰 إدارة المعاملات المالية للوسطاء (Broker Transactions) ===
class BrokerTransactionListCreateView(BaseListView):
    """
    ✅ إنشاء وعرض قائمة المعاملات المالية للوسطاء مع دعم البحث والترتيب والتصفية.
    """
    queryset = BrokerTransaction.objects.all().order_by('-transaction_date')
    serializer_class = BrokerTransactionSerializer
    search_fields = ['broker__name', 'transaction_type']
    ordering_fields = ['transaction_date', 'amount']
    filterset_fields = ['broker', 'transaction_type', 'transaction_date']


class BrokerTransactionDetailView(BaseDetailView):
    """
    ✅ عرض وتحديث وحذف معاملة مالية معينة للوسيط.
    """
    queryset = BrokerTransaction.objects.all()
    serializer_class = BrokerTransactionSerializer


# === 📊 إدارة تقييم أداء الموظفين (Employee Performance) ===
class EmployeePerformanceListCreateView(BaseListView):
    """
    ✅ عرض قائمة أداء الموظفين وإمكانية إنشاء سجل جديد.
    """
    queryset = EmployeePerformance.objects.all()
    serializer_class = EmployeePerformanceSerializer


class EmployeePerformanceDetailView(BaseDetailView):
    """
    ✅ عرض وتحديث وحذف سجل أداء موظف معين.
    """
    queryset = EmployeePerformance.objects.all()
    serializer_class = EmployeePerformanceSerializer
