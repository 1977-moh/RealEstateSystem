from django.contrib import admin
from .models import Broker, BrokerClient, BrokerTransaction

# ✅ تجنب تسجيل EmployeePerformance مرتين لأنه مسجل في `employees/admin.py`
@admin.register(Broker)
class BrokerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "commission_rate", "total_earnings", "created_at")
    search_fields = ("name", "email")


@admin.register(BrokerClient)
class BrokerClientAdmin(admin.ModelAdmin):
    list_display = ("client", "broker", "status", "assigned_date", "expiry_date")
    search_fields = ("client__name", "broker__name")


@admin.register(BrokerTransaction)
class BrokerTransactionAdmin(admin.ModelAdmin):
    list_display = ("broker", "transaction_type", "amount", "transaction_date")
    search_fields = ("broker__name", "transaction_type")
