from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    days_since_entry = serializers.SerializerMethodField()  # حقل محسوب

    class Meta:
        model = Client
        fields = '__all__'

    def validate_phone(self, value):
        """التحقق من أن رقم الهاتف يحتوي فقط على أرقام."""
        if value and not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def get_days_since_entry(self, obj):
        """إرجاع عدد الأيام منذ إدخال العميل."""
        from datetime import datetime
        if obj.entry_date:
            delta = datetime.now().date() - obj.entry_date.date()
            return delta.days
        return None
