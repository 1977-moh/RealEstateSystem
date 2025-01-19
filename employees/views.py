from rest_framework import generics, permissions
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListView(generics.ListCreateAPIView):
    """
    عرض قائمة الموظفين أو إضافة موظف جديد.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المصادق عليهم

    def get_queryset(self):
        """
        تخصيص البيانات المرتجعة مع دعم التصفية.
        """
        queryset = Employee.objects.all().order_by('-created_at')  # ترتيب السجلات حسب الأحدث
        department = self.request.query_params.get('department')  # تصفية حسب القسم
        role = self.request.query_params.get('role')  # تصفية حسب الدور
        if department:
            queryset = queryset.filter(department=department)
        if role:
            queryset = queryset.filter(role=role)
        return queryset


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض، تحديث، أو حذف موظف معين.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح فقط للمستخدمين المصادق عليهم

    def get_queryset(self):
        """
        تخصيص البيانات المرتجعة للموظف.
        """
        return Employee.objects.all()

    def perform_update(self, serializer):
        """
        تخصيص عملية التحديث.
        """
        serializer.save()  # تنفيذ عملية الحفظ
