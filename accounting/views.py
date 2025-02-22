from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Salary, Bonus, Deduction, SalesCommission
from .serializers import SalarySerializer, BonusSerializer, DeductionSerializer, SalesCommissionSerializer


class CustomPagination(PageNumberPagination):
    """
    ✅ إعداد التصفح (Pagination) بحيث يكون عدد العناصر في الصفحة 10.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


# === 🏆 إدارة المرتبات (Salaries) ===
class SalaryListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة المرتبات أو إضافة مرتب جديد.
    - دعم البحث والتصفية والفرز.
    """
    queryset = Salary.objects.all().order_by('-created_at')
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['employee__full_name']
    filterset_fields = ['employee']
    ordering_fields = ['base_salary', 'created_at', 'updated_at']


class SalaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تعديل أو حذف مرتب معين.
    - السماح فقط للمستخدمين المصادق عليهم.
    - السماح للمسؤولين فقط بالحذف.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [permissions.IsAuthenticated]


# === 🎁 إدارة المكافآت (Bonuses) ===
class BonusListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة المكافآت أو إضافة مكافأة جديدة.
    """
    queryset = Bonus.objects.all().order_by('-date_given')
    serializer_class = BonusSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['employee__full_name', 'reason']
    filterset_fields = ['employee', 'date_given']
    ordering_fields = ['amount', 'date_given']


class BonusDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تعديل أو حذف مكافأة معينة.
    """
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    permission_classes = [permissions.IsAuthenticated]


# === 📉 إدارة الخصومات (Deductions) ===
class DeductionListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة الخصومات أو إضافة خصم جديد.
    """
    queryset = Deduction.objects.all().order_by('-date_given')
    serializer_class = DeductionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['employee__full_name', 'reason']
    filterset_fields = ['employee', 'date_given']
    ordering_fields = ['amount', 'date_given']


class DeductionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تعديل أو حذف خصم معين.
    """
    queryset = Deduction.objects.all()
    serializer_class = DeductionSerializer
    permission_classes = [permissions.IsAuthenticated]


# === 💰 إدارة العمولات (Sales Commissions) ===
class SalesCommissionListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة العمولات أو إضافة عمولة جديدة.
    """
    queryset = SalesCommission.objects.all().order_by('-date_calculated')
    serializer_class = SalesCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['employee__full_name']
    filterset_fields = ['employee', 'date_calculated']
    ordering_fields = ['sales_amount', 'commission_earned', 'date_calculated']


class SalesCommissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تعديل أو حذف عمولة معينة.
    """
    queryset = SalesCommission.objects.all()
    serializer_class = SalesCommissionSerializer
    permission_classes = [permissions.IsAuthenticated]
