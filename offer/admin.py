from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """
    ✅ لوحة تحكم العروض في Django Admin
    """
    # ✅ تحسين عرض القائمة الرئيسية بإضافة معلومات أكثر
    list_display = ['title', 'offer_type', 'value', 'status', 'assigned_employee', 'start_date', 'end_date', 'is_active', 'created_at']

    # ✅ تحسين التصفية لتسهيل البحث داخل Django Admin
    list_filter = ['offer_type', 'status', 'is_active', 'start_date', 'end_date']

    # ✅ تمكين البحث حسب العنوان، الوصف، واسم الموظف المسؤول
    search_fields = ['title', 'description', 'assigned_employee__username']

    # ✅ تحسين ترتيب السجلات بحيث تظهر الأحدث أولًا
    ordering = ['-created_at']

    # ✅ تمكين التعديل المباشر على `is_active` و `status`
    list_editable = ['is_active', 'status']

    # ✅ جعل الحقول الزمنية للقراءة فقط
    readonly_fields = ['created_at', 'updated_at']

    # ✅ تحديد عدد العروض في كل صفحة
    list_per_page = 20

    # ✅ تنظيم الحقول بطريقة أكثر وضوحًا داخل Django Admin
    fieldsets = (
        ("🔹 تفاصيل العرض", {
            'fields': ('title', 'description', 'offer_type', 'value', 'status', 'is_active')
        }),
        ("🏢 العقارات والعملاء", {
            'fields': ('properties', 'clients')
        }),
        ("👤 المسؤول", {
            'fields': ('assigned_employee',)
        }),
        ("📅 المدة الزمنية", {
            'fields': ('start_date', 'end_date')
        }),
        ("🕒 معلومات التوقيت", {
            'fields': ('created_at', 'updated_at')
        }),
    )
