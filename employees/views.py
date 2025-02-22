from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Count
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeePagination(PageNumberPagination):
    """
    ✅ إعداد التصفح (Pagination) بحيث يكون عدد العناصر في الصفحة 10.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class EmployeeListView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة الموظفين أو إضافة موظف جديد.
    - دعم البحث حسب `full_name` و `email`
    - دعم الفلترة حسب `department` و `role` و `status`
    - دعم الترتيب حسب `hire_date` و `created_at`
    """
    queryset = Employee.objects.all().order_by('-created_at')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = EmployeePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # ✅ تحديد حقول البحث والفلترة والفرز
    search_fields = ['full_name', 'email']
    filterset_fields = ['department', 'role', 'status']
    ordering_fields = ['hire_date', 'created_at', 'role']

    def get_queryset(self):
        """
        ✅ تخصيص البيانات بناءً على صلاحيات المستخدم.
        """
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(department=self.request.user.department)

        return queryset

    def perform_create(self, serializer):
        """
        ✅ تسجيل المستخدم الذي أضاف الموظف.
        """
        serializer.save(created_by=self.request.user)


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض، تحديث، أو حذف موظف معين.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        ✅ تسجيل المستخدم الذي قام بالتحديث، ومنع تغيير دور المستخدم العادي.
        """
        instance = self.get_object()

        if not self.request.user.is_superuser:
            restricted_fields = ['role', 'status']
            for field in restricted_fields:
                if field in self.request.data:
                    raise permissions.PermissionDenied(f"🚨 You cannot update `{field}`.")

        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        """
        ✅ منع حذف المسؤول الأخير داخل الشركة.
        """
        if instance.role == "Admin":
            admin_count = Employee.objects.filter(role="Admin").count()
            if admin_count <= 1:
                raise permissions.PermissionDenied("🚨 Cannot delete the last Admin!")

        if not self.request.user.is_superuser:
            raise permissions.PermissionDenied("🚨 Only admins can delete employees.")

        instance.delete()


class EmployeeStatsView(APIView):
    """
    ✅ إحصائيات عامة عن الموظفين.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        ✅ إرجاع إحصائيات الموظفين.
        """
        stats = {
            "total_employees": Employee.objects.count(),
            "employees_by_department": {
                entry['department__name']: entry['total']
                for entry in Employee.objects.values('department__name').annotate(total=Count('id'))
            },
            "employees_by_status": {
                entry['status']: entry['total']
                for entry in Employee.objects.values('status').annotate(total=Count('id'))
            },
            "employees_by_role": {
                entry['role']: entry['total']
                for entry in Employee.objects.values('role').annotate(total=Count('id'))
            },
        }
        return Response(stats, status=status.HTTP_200_OK)


class EmployeeStatusUpdateView(APIView):
    """
    ✅ تحديث حالة الموظف (نشط/غير نشط) - يسمح فقط للمسؤولين بتحديث الحالة.
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        """
        ✅ تحديث حالة الموظف.
        """
        try:
            employee = Employee.objects.get(pk=pk)
            new_status = request.data.get("status")

            if new_status not in ["Active", "Inactive", "On Leave", "Retired"]:
                return Response({"error": "🚨 Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

            employee.status = new_status
            employee.save()
            return Response({"message": "✅ Employee status updated successfully."}, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "❌ Employee not found."}, status=status.HTTP_404_NOT_FOUND)


class EmployeeBulkCreateView(APIView):
    """
    ✅ إضافة عدة موظفين دفعة واحدة.
    """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """
        ✅ استقبال بيانات عدة موظفين دفعة واحدة.
        """
        employees_data = request.data.get("employees", [])

        if not employees_data:
            return Response({"error": "❌ No employees data provided."}, status=status.HTTP_400_BAD_REQUEST)

        errors = []
        created_employees = []

        for employee_data in employees_data:
            serializer = EmployeeSerializer(data=employee_data)

            if serializer.is_valid():
                serializer.save()
                created_employees.append(serializer.data)
            else:
                errors.append({"data": employee_data, "errors": serializer.errors})

        if errors:
            return Response({
                "message": "⚠️ Some employees were not created due to validation errors.",
                "created_employees": created_employees,
                "errors": errors
            }, status=status.HTTP_206_PARTIAL_CONTENT)

        return Response({
            "message": "✅ All employees created successfully.",
            "created_employees": created_employees
        }, status=status.HTTP_201_CREATED)
