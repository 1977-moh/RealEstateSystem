from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    ✅ إدارة واجهة العملاء (Client) في لوحة إدارة Django.
    """

    # ✅ عرض الأعمدة الرئيسية
    list_display = ['id', 'name', 'email', 'phone', 'location', 'status', 'entry_date', 'created_at']
    list_filter = ['status', 'entry_date', 'created_at', 'location']  # ✅ دعم التصفية حسب الحالة
    search_fields = ['id', 'name', 'email', 'phone']  # ✅ دعم البحث عن العملاء باستخدام `UUID`
    ordering = ['-created_at']  # ✅ ترتيب افتراضي حسب الأحدث

    # ✅ الحقول للقراءة فقط
    readonly_fields = ['id', 'entry_date', 'created_at', 'updated_at']

    # ✅ تنظيم الحقول في مجموعات مع تعليمات مساعدة
    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'email', 'phone', 'location', 'status', 'interests'),
            'description': "الحقول الأساسية التي تحدد معلومات العميل."
        }),
        ("Details", {
            'fields': ('client_request_details', 'address'),
            'description': "تفاصيل إضافية عن طلبات العميل وعنوانه."
        }),
        ("Timestamps", {
            'fields': ('id', 'entry_date', 'created_at', 'updated_at'),
            'description': "المعرف الفريد والوقت الزمني لإدخال وإنشاء وتحديث العميل."
        }),
    )

    # ✅ تحسين واجهة إدارة Django
    list_per_page = 20  # عدد السجلات في الصفحة الواحدة
    date_hierarchy = 'created_at'  # ✅ إضافة شريط زمني أعلى القائمة للبحث بالتاريخ
