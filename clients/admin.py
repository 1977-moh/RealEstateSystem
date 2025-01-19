from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # عرض الأعمدة في لوحة الإدارة
    list_display = ['name', 'email', 'phone', 'location', 'entry_date', 'created_at']

    # إضافة خيارات التصفية
    list_filter = ['entry_date', 'created_at', 'location']

    # تمكين البحث
    search_fields = ['name', 'email', 'phone']

    # تحديد ترتيب السجلات افتراضيًا
    ordering = ['-created_at']

    # جعل الحقول غير قابلة للتعديل
    readonly_fields = ['entry_date', 'created_at', 'updated_at']

    # تنظيم الحقول في مجموعات
    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'email', 'phone', 'location', 'interests')
        }),
        ("Details", {
            'fields': ('client_request_details', 'address')
        }),
        ("Timestamps", {
            'fields': ('entry_date', 'created_at', 'updated_at')
        }),
    )

    # عدد السجلات في الصفحة الواحدة
    list_per_page = 20
