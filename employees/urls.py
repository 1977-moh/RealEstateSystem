from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

# تعريف Namespace للتطبيق
app_name = 'employees'

# المسارات
urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),  # عرض قائمة الموظفين وإضافة موظف جديد
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),  # عرض/تحديث/حذف موظف معين
]
