from django.contrib import admin
from django.apps import apps  # ✅ تجنب الاستيراد الدائري

# ✅ استيراد النماذج بطريقة ديناميكية لتجنب `ImportError`
JobTitle = apps.get_model('accounting', 'JobTitle')
Department = apps.get_model('accounting', 'Department')
IncentiveType = apps.get_model('accounting', 'IncentiveType')
DeductionType = apps.get_model('accounting', 'DeductionType')
Salary = apps.get_model('accounting', 'Salary')
Bonus = apps.get_model('accounting', 'Bonus')
Deduction = apps.get_model('accounting', 'Deduction')
SalesCommission = apps.get_model('accounting', 'SalesCommission')


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(IncentiveType)
class IncentiveTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(DeductionType)
class DeductionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ['employee', 'base_salary', 'commission_rate', 'tax_deduction', 'created_at']
    list_filter = ['commission_rate', 'tax_deduction', 'created_at']
    search_fields = ['employee__full_name']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']  # ✅ جعل الحقول الزمنية غير قابلة للتعديل

    fieldsets = (
        ("Salary Details", {
            'fields': ('employee', 'base_salary', 'commission_rate', 'commission_fixed', 'tax_deduction')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'reason', 'date_given']
    list_filter = ['date_given']
    search_fields = ['employee__full_name', 'reason']
    ordering = ['-date_given']
    readonly_fields = ['date_given']  # ✅ منع تعديل تاريخ المكافأة بعد إضافتها

    fieldsets = (
        ("Bonus Information", {
            'fields': ('employee', 'amount', 'reason', 'date_given')
        }),
    )


@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'amount', 'reason', 'date_given']
    list_filter = ['date_given']
    search_fields = ['employee__full_name', 'reason']
    ordering = ['-date_given']
    readonly_fields = ['date_given']  # ✅ منع تعديل تاريخ الخصم بعد إضافته

    fieldsets = (
        ("Deduction Information", {
            'fields': ('employee', 'amount', 'reason', 'date_given')
        }),
    )


@admin.register(SalesCommission)
class SalesCommissionAdmin(admin.ModelAdmin):
    list_display = ['employee', 'sales_amount', 'commission_earned', 'date_calculated']
    list_filter = ['date_calculated']
    search_fields = ['employee__full_name']
    ordering = ['-date_calculated']
    readonly_fields = ['date_calculated']  # ✅ منع تعديل تاريخ العمولات بعد حسابها

    fieldsets = (
        ("Commission Details", {
            'fields': ('employee', 'sales_amount', 'commission_earned', 'date_calculated')
        }),
    )
