from django.contrib import admin
from .models import Campaign
from datetime import date


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    """
    ✅ تحسين واجهة إدارة الحملات داخل Django Admin.
    """

    # ✅ عرض الأعمدة الرئيسية مع الحقول المحسوبة
    list_display = (
        'id', 'name', 'platform', 'budget', 'daily_budget', 'start_date', 'end_date', 'days_remaining', 'status'
    )

    # ✅ إضافة خيارات التصفية
    list_filter = ('platform', 'status', 'start_date', 'end_date')

    # ✅ تحسين البحث ليشمل المنصة والحالة أيضًا
    search_fields = ('name', 'platform', 'status')

    # ✅ منع تعديل بعض الحقول
    readonly_fields = ('id', 'campaign_url', 'created_at', 'updated_at')

    # ✅ تنظيم الحقول في مجموعات داخل Django Admin
    fieldsets = (
        ("Campaign Details", {
            "fields": ('id', 'name', 'platform', 'description', 'campaign_url')
        }),
        ("Financials", {
            "fields": ('budget', 'daily_budget')
        }),
        ("Schedule", {
            "fields": ('start_date', 'end_date', 'days_remaining', 'status')
        }),
        ("Timestamps", {
            "fields": ('created_at', 'updated_at')
        }),
    )

    @admin.display(description="Days Remaining")
    def days_remaining(self, obj):
        """
        ✅ إرجاع عدد الأيام المتبقية حتى انتهاء الحملة.
        ✅ التأكد من أن `end_date` أكبر من `start_date` لمنع الأخطاء.
        """
        if obj.end_date and obj.start_date and obj.end_date >= obj.start_date:
            remaining_days = (obj.end_date - date.today()).days
            return max(remaining_days, 0)
        return "❌ Invalid Dates"

    @admin.display(description="Daily Budget ($)")
    def daily_budget(self, obj):
        """
        ✅ إرجاع الميزانية اليومية بناءً على عدد أيام الحملة.
        ✅ التأكد من أن `end_date` أكبر من `start_date` لمنع القسمة على الصفر.
        """
        if obj.end_date and obj.start_date and obj.end_date > obj.start_date:
            total_days = (obj.end_date - obj.start_date).days
            return round(obj.budget / total_days, 2) if total_days > 0 else "❌ Invalid Budget"
        return "❌ Invalid Dates"
