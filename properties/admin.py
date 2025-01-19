from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'location', 'price', 'developer', 'created_at']
    list_filter = ['property_type', 'payment_method', 'developer', 'created_at']
    search_fields = ['location', 'developer', 'description']
