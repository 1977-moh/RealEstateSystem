from django.contrib import admin
from django.db import models
from .models import Employee, Department, JobTitle, EmployeePerformance  # ✅ تأكد من استيراد جميع الموديلات ذات العلاقة
from datetime import date


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """✅ لوحة تحكم إدارة الأقسام."""
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    """✅ لوحة تحكم إدارة المسميات الوظيفية."""
    list_display = ['id', 'title']
    search_fields = ['title']
    ordering = ['title']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """✅ لوحة تحكم الموظفين في Django Admin مع تحسينات في العرض والبحث."""

    list_display = [
        'id', 'full_name', 'email', 'phone', 'department', 'status', 'hire_date', 'years_of_service', 'created_at'
    ]

    list_editable = ['department', 'status']  # ✅ أزل `role` إذا لم يكن موجودًا
    list_filter = ['department', 'status', 'hire_date', 'created_at']
    search_fields = ['full_name', 'email', 'phone']
    ordering = ['-hire_date', '-created_at']
    date_hierarchy = 'hire_date'
    readonly_fields = ['id', 'created_at', 'updated_at', 'hire_date']
    fieldsets = (
        ("Basic Information", {'fields': ('full_name', 'email', 'phone')}),
        ("Job Details", {'fields': ('department', 'hire_date', 'status')}),
        ("Timestamps", {'fields': ('id', 'created_at', 'updated_at')}),
    )

    autocomplete_fields = ['department']
    save_on_top = True
    save_as = True
    list_per_page = 20
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        """✅ تفعيل الموظفين المحددين."""
        queryset.update(status='Active')
        self.message_user(request, "✅ تم تنشيط الموظفين المحددين.")

    make_active.short_description = "🔵 تنشيط الموظفين المحددين"

    def make_inactive(self, request, queryset):
        """✅ إلغاء تنشيط الموظفين المحددين."""
        queryset.update(status='Inactive')
        self.message_user(request, "⛔ تم تعطيل الموظفين المحددين.")

    make_inactive.short_description = "🔴 تعطيل الموظفين المحددين"

    def years_of_service(self, obj):
        """✅ حساب عدد سنوات الخدمة بناءً على `hire_date`."""
        today = date.today()
        return today.year - obj.hire_date.year if obj.hire_date else "N/A"

    years_of_service.short_description = "Years of Service"


@admin.register(EmployeePerformance)
class EmployeePerformanceAdmin(admin.ModelAdmin):
    """✅ لوحة تحكم إدارة تقييمات أداء الموظفين."""

    list_display = ['employee', 'review_date', 'rewards',
                    'penalties']  # ✅ أزل `broker` إذا لم يكن في `EmployeePerformance`
    list_filter = ['review_date', 'employee__department']
    search_fields = ['employee__full_name']
    ordering = ['-review_date']
    readonly_fields = ['review_date']
