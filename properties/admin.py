from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    ✅ تخصيص لوحة التحكم لإدارة العقارات.
    """

    # ✅ عرض الحقول الرئيسية في قائمة العقارات
    list_display = ['id', 'property_type', 'location', 'price', 'developer', 'created_at']

    # ✅ إضافة خيارات التصفية
    list_filter = ['property_type', 'payment_method', 'developer', 'price', 'delivery_date', 'payment_percentage_for_delivery', 'created_at']

    # ✅ تحسين البحث ليشمل UUID والموقع والمطور والوصف والسعر
    search_fields = ['id', 'location', 'developer', 'description', 'price']

    # ✅ منع تعديل الحقول الزمنية و UUID
    readonly_fields = ['id', 'created_at', 'updated_at']

    # ✅ ترتيب العقارات افتراضيًا حسب الأحدث
    ordering = ['-created_at']

    # ✅ تنظيم الحقول في صفحة تفاصيل العقار
    fieldsets = (
        ("Basic Information", {
            'fields': ('id', 'property_type', 'location', 'developer', 'description')
        }),
        ("Financial Details", {
            'fields': ('price', 'payment_method', 'maintenance_value_type', 'maintenance_value')
        }),
        ("Delivery Information", {
            'fields': ('delivery_method', 'delivery_date', 'payment_percentage_for_delivery')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # ✅ تحديد عدد السجلات في كل صفحة
    list_per_page = 20
