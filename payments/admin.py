from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    ✅ إدارة لوحة تحكم المدفوعات في Django Admin.
    """
    # ✅ عرض الأعمدة في القائمة الرئيسية
    list_display = ['id', 'amount', 'method', 'short_description', 'date', 'created_at', 'updated_at']

    # ✅ إضافة خيارات التصفية
    list_filter = ['method', 'date', 'amount']

    # ✅ تمكين البحث
    search_fields = ['id', 'description', 'amount', 'method', 'date', 'created_at']

    # ✅ تمكين ترتيب السجلات
    ordering = ['-date', '-created_at']

    # ✅ جعل بعض الحقول قابلة للتعديل مباشرة من القائمة
    list_editable = ['amount', 'method']

    # ✅ الحقول التي لا يمكن تعديلها
    readonly_fields = ['created_at', 'updated_at']

    # ✅ إضافة تصفح زمني (تقويم) حسب تاريخ الدفع
    date_hierarchy = 'date'

    # ✅ تنظيم الحقول في مجموعات لعرض أفضل
    fieldsets = (
        ("🔹 تفاصيل الدفع", {
            'fields': ('amount', 'method', 'date', 'description')
        }),
        ("🕒 معلومات التوقيت", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # ✅ تحديد عدد السجلات في الصفحة الواحدة
    list_per_page = 20

    @admin.display(description="Description")
    def short_description(self, obj):
        """
        ✅ عرض وصف مختصر للدفعة.
        """
        return obj.description[:30] + "..." if obj.description and len(obj.description) > 30 else obj.description
