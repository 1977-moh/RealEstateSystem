from django.contrib import admin
from .models import DashboardStats

@admin.register(DashboardStats)
class DashboardStatsAdmin(admin.ModelAdmin):
    """
    ✅ لوحة تحكم إحصائيات Dashboard في Django Admin.
    """
    list_display = ('total_clients', 'total_properties', 'total_sales', 'active_campaigns', 'last_updated')
    readonly_fields = ('last_updated',)  # ✅ منع تعديل وقت التحديث
    ordering = ('-last_updated',)
