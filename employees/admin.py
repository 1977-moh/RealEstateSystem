from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # عرض الأعمدة في قائمة الموظفين
    list_display = ['full_name', 'email', 'phone', 'role', 'department', 'status', 'hire_date', 'created_at']

    # خيارات التصفية
    list_filter = ['department', 'role', 'status', 'hire_date']

    # تمكين البحث
    search_fields = ['full_name', 'email', 'phone']

    # ترتيب السجلات
    ordering = ['-hire_date']

    # حقول للقراءة فقط
    readonly_fields = ['created_at', 'updated_at']

    # تنظيم الحقول في صفحة تفاصيل الموظف
    fieldsets = (
        ("Basic Information", {
            'fields': ('full_name', 'email', 'phone')
        }),
        ("Job Details", {
            'fields': ('role', 'department', 'hire_date', 'status')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # عدد السجلات في الصفحة الواحدة
    list_per_page = 20
