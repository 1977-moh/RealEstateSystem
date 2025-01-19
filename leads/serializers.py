from rest_framework import serializers
from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer لتحويل بيانات Lead إلى JSON والعكس.
    """
    class Meta:
        model = Lead
        fields = '__all__'  # تضمين جميع الحقول
        read_only_fields = ('created_at', 'updated_at')  # جعل الحقول الزمنية للقراءة فقط

    def validate_phone(self, value):
        """
        التحقق من صحة حقل الهاتف.
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain digits only.")
        return value

    def validate_email(self, value):
        """
        التحقق من صحة حقل البريد الإلكتروني (تجنب النسخ المكررة).
        """
        if Lead.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already used by another lead.")
        return value
