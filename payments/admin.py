from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['amount', 'method', 'date', 'created_at']
    list_filter = ['method', 'date']
    search_fields = ['description']
from django.contrib import admin

# Register your models here.
