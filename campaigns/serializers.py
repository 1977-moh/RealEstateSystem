from rest_framework import serializers
from .models import Campaign
from datetime import date

class CampaignSerializer(serializers.ModelSerializer):
    days_remaining = serializers.SerializerMethodField()  # حقل مخصص لحساب الأيام المتبقية

    class Meta:
        model = Campaign
        fields = '__all__'

    def validate(self, data):
        """التحقق من تواريخ البداية والنهاية."""
        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("End date must be later than start date.")
        return data

    def validate_budget(self, value):
        """التحقق من أن الميزانية موجبة."""
        if value <= 0:
            raise serializers.ValidationError("Budget must be a positive number.")
        return value

    def get_days_remaining(self, obj):
        """إرجاع عدد الأيام المتبقية."""
        return (obj.end_date - date.today()).days if obj.end_date >= date.today() else 0
