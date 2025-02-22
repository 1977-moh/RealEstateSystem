from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات Payment إلى JSON والعكس.
    """
    detailed_description = serializers.SerializerMethodField()  # ✅ وصف تفصيلي للدفعة
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات

    MAX_PAYMENT_USD = 1_000_000.00  # ✅ الحد الأقصى بالدولار
    MAX_PAYMENT_EGP = 30_000_000.00  # ✅ الحد الأقصى بالجنيه المصري

    class Meta:
        model = Payment
        fields = '__all__'  # ✅ تضمين جميع الحقول
        extra_kwargs = {
            'created_at': {'read_only': True},  # ✅ جعل الحقل للقراءة فقط
            'updated_at': {'read_only': True}
        }

    def validate_amount(self, value):
        """
        ✅ التحقق من صحة قيمة المبلغ بناءً على العملة.
        """
        if value <= 0:
            raise serializers.ValidationError("🚨 The payment amount must be greater than zero.")

        # ✅ التأكد من الحد الأقصى للمبلغ بناءً على العملة المختارة
        currency = self.initial_data.get("currency", "EGP")
        max_amount = self.MAX_PAYMENT_EGP if currency == "EGP" else self.MAX_PAYMENT_USD

        if value > max_amount:
            raise serializers.ValidationError(f"🚨 The maximum allowed payment amount for {currency} is {max_amount:,.2f}.")

        return value

    def validate_method(self, value):
        """
        ✅ التحقق من صحة طريقة الدفع باستخدام الخيارات المتاحة في الموديل.
        """
        valid_methods = dict(Payment.PAYMENT_METHODS).keys()
        if value not in valid_methods:
            raise serializers.ValidationError(
                f"🚨 Invalid payment method. Choose from {list(valid_methods)}."
            )
        return value

    def get_detailed_description(self, obj):
        """
        ✅ إرجاع وصف تفصيلي للدفعة يشمل العملة.
        """
        currency_symbol = "ج.م" if obj.currency == "EGP" else "$"
        recent = "✅ Recent Payment" if obj.is_recent_payment() else "📅 Old Payment"
        return f"{recent} 💳 Payment of {currency_symbol}{obj.amount:,.2f} via {obj.method} on {obj.date.strftime('%Y-%m-%d')}"
