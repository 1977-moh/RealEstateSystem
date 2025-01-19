from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer لتحويل بيانات Payment إلى JSON والعكس.
    """
    detailed_description = serializers.SerializerMethodField()  # حقل مخصص

    class Meta:
        model = Payment
        fields = '__all__'  # تضمين جميع الحقول
        read_only_fields = ('created_at', 'updated_at')  # جعل الحقول الزمنية للقراءة فقط

    def get_detailed_description(self, obj):
        """
        إرجاع وصف مفصل للدفعة.
        """
        return f"Payment of {obj.amount} via {obj.method} on {obj.date}"

    def validate_amount(self, value):
        """
        التحقق من صحة قيمة المبلغ.
        """
        if value <= 0:
            raise serializers.ValidationError("The payment amount must be greater than zero.")
        return value
