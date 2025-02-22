from django.urls import path
from .views import (
    EmployeeListView, EmployeeDetailView, EmployeeStatsView,
    EmployeeStatusUpdateView, EmployeeBulkCreateView
)

# ✅ تحديد اسم المساحة (Namespace) للتطبيق
app_name = 'employees'

# ✅ تعريف المسارات مع دعم التصفية عبر `query parameters`
urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),  # ✅ عرض قائمة الموظفين وإضافة موظف جديد
    path('<uuid:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),  # ✅ عرض/تحديث/حذف موظف معين
    path('stats/', EmployeeStatsView.as_view(), name='employee-stats'),  # ✅ عرض إحصائيات الموظفين
    path('<uuid:pk>/status/', EmployeeStatusUpdateView.as_view(), name='employee-status-update'),  # ✅ تحديث حالة الموظف
    path('bulk-create/', EmployeeBulkCreateView.as_view(), name='employee-bulk-create'),  # ✅ إضافة عدة موظفين دفعة واحدة
]
