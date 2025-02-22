from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    ✅ لوحة تحكم لإعدادات الموقع، تتيح تعديل المعلومات ولكن تمنع إضافة أكثر من إدخال واحد.
    """
    list_display = ('site_name', 'contact_email', 'phone_number', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # ✅ جعل الحقول الزمنية غير قابلة للتعديل

    fieldsets = (
        ("Basic Info", {
            'fields': ('site_name', 'logo')
        }),
        ("Contact Details", {
            'fields': ('contact_email', 'phone_number', 'address')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def has_add_permission(self, request):
        """
        ✅ منع إضافة أكثر من سجل واحد.
        """
        return not SiteSettings.objects.exists()

    def has_change_permission(self, request, obj=None):
        """
        ✅ السماح بالتعديل فقط إذا كان هناك سجل موجود.
        """
        return SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """
        ✅ منع حذف السجل.
        """
        return False

    def get_queryset(self, request):
        """
        ✅ عرض إدخال واحد فقط في Django Admin.
        """
        return super().get_queryset(request)[:1]  # ✅ عرض أول إدخال فقط

    def get_object(self, request, object_id=None):
        """
        ✅ التأكد من أن هناك إدخال واحد فقط، وإذا لم يوجد يتم إنشاؤه تلقائيًا.
        """
        obj, created = SiteSettings.objects.get_or_create()
        return obj
