from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now
from datetime import date, timedelta
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """
    ✅ لوحة تحكم Django Admin لإدارة العملاء المتوقعين (Leads).
    """

    # ✅ عرض الأعمدة الرئيسية مع تحسينات الذكاء الصناعي
    list_display = (
        'id', 'colored_status', 'name', 'email', 'phone', 'short_campaign_name',
        'assigned_to', 'lead_score', 'days_since_creation', 'created_at'
    )

    # ✅ إضافة خيارات التصفية حسب المدة الزمنية
    list_filter = ('status', 'campaign__end_date', 'assigned_to', ('created_at', admin.DateFieldListFilter))

    # ✅ تحسين البحث ليشمل الحملة والموظف المسؤول أيضًا
    search_fields = ('name', 'email', 'phone', 'campaign__name', 'assigned_to__full_name')

    # ✅ منع تعديل بعض الحقول
    readonly_fields = ('id', 'created_at', 'updated_at', 'lead_score')

    # ✅ تنظيم الحقول في مجموعات داخل Django Admin
    fieldsets = (
        ("Lead Information", {
            "fields": ('id', 'name', 'email', 'phone', 'campaign', 'assigned_to', 'status', 'lead_score')
        }),
        ("Timestamps", {
            "fields": ('created_at', 'updated_at')
        }),
    )

    # ✅ تحديد عدد السجلات في كل صفحة
    list_per_page = 20

    # ✅ خيارات الإجراءات المخصصة في لوحة التحكم
    actions = ['mark_as_converted', 'mark_as_closed']

    @admin.display(description="Days Since Created")
    def days_since_creation(self, obj):
        """
        ✅ إرجاع عدد الأيام منذ إنشاء العميل المحتمل.
        """
        return (date.today() - obj.created_at.date()).days

    @admin.display(description="Campaign")
    def short_campaign_name(self, obj):
        """
        ✅ اختصار اسم الحملة في حالة كان طويلاً.
        """
        return obj.campaign.name[:15] + "..." if len(obj.campaign.name) > 15 else obj.campaign.name

    @admin.display(description="Lead Score", ordering='lead_score')
    def lead_score(self, obj):
        """
        ✅ إظهار تقييم الذكاء الاصطناعي (`Lead Score`).
        """
        return format_html(
            f'<b style="color: {"#4CAF50" if obj.lead_score > 80 else "#FFC107" if obj.lead_score > 50 else "#F44336"};">'
            f'{obj.lead_score}%</b>'
        )

    @admin.display(description="Status")
    def colored_status(self, obj):
        """
        ✅ تلوين حالة العميل (`New`, `In Progress`, `Converted`) لسهولة المتابعة.
        """
        status_colors = {
            "New": "#2196F3",  # Blue
            "In Progress": "#FFC107",  # Yellow
            "Converted": "#4CAF50",  # Green
            "Closed": "#F44336",  # Red
        }
        return format_html(
            f'<span style="color: {status_colors.get(obj.status, "#000")}; font-weight: bold;">{obj.status}</span>'
        )

    def mark_as_converted(self, request, queryset):
        """
        ✅ إجراء مخصص لتحويل العملاء المحتملين إلى `Converted`.
        """
        queryset.update(status="Converted")
        self.message_user(request, "✅ تم تحويل العملاء المحددين إلى 'Converted'.")

    mark_as_converted.short_description = "✅ تحويل إلى Converted"

    def mark_as_closed(self, request, queryset):
        """
        ✅ إجراء مخصص لإغلاق العملاء المحتملين.
        """
        queryset.update(status="Closed")
        self.message_user(request, "❌ تم إغلاق العملاء المحددين.")

    mark_as_closed.short_description = "❌ إغلاق Leads"


