from rest_framework import serializers
from .models import Offer
from datetime import date


class OfferSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات Offer إلى JSON والعكس.
    """

    offer_type_display = serializers.SerializerMethodField()  # ✅ عرض نوع العرض بوصف واضح
    days_remaining = serializers.SerializerMethodField()  # ✅ حساب عدد الأيام المتبقية للعرض
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات

    MAX_OFFER_VALUE_USD = 1_000_000.00  # ✅ الحد الأقصى للقيمة بالدولار
    MAX_OFFER_VALUE_EGP = 30_000_000.00  # ✅ الحد الأقصى للقيمة بالجنيه المصري

    class Meta:
        model = Offer
        fields = '__all__'  # ✅ تضمين جميع الحقول
        read_only_fields = ('created_at', 'updated_at')  # ✅ الحقول الزمنية للقراءة فقط

    def validate_value(self, value):
        """
        ✅ التحقق من أن قيمة العرض موجبة وليست غير منطقية بناءً على العملة المختارة.
        """
        if value <= 0:
            raise serializers.ValidationError("🚨 Offer value must be greater than zero.")

        currency = self.initial_data.get("currency", "EGP")
        max_value = self.MAX_OFFER_VALUE_EGP if currency == "EGP" else self.MAX_OFFER_VALUE_USD

        if value > max_value:
            raise serializers.ValidationError(f"🚨 The maximum allowed offer value for {currency} is {max_value:,.2f}.")
        return value

    def validate(self, data):
        """
        ✅ التحقق من صحة تواريخ البداية والنهاية ومنع تعديل `start_date` بعد الحفظ.
        """
        instance = getattr(self, 'instance', None)

        if instance and 'start_date' in data and data['start_date'] != instance.start_date:
            raise serializers.ValidationError("🚨 Start date cannot be modified after creation.")

        if data['end_date'] <= data['start_date']:
            raise serializers.ValidationError("🚨 End date must be later than start date.")

        return data

    def get_offer_type_display(self, obj):
        """
        ✅ إرجاع وصف أوضح لنوع العرض.
        """
        return dict(Offer.OFFER_TYPE_CHOICES).get(obj.offer_type, "Unknown")

    def get_days_remaining(self, obj):
        """
        ✅ إرجاع عدد الأيام المتبقية للعرض أو "Expired" إذا كان العرض منتهيًا.
        """
        remaining_days = (obj.end_date - date.today()).days if obj.end_date else None
        return remaining_days if remaining_days and remaining_days > 0 else "Expired"

    def send_offer(self, method):
        """
        ✅ إرسال العرض إلى العميل عبر:
        - 📄 **الطباعة**
        - 📧 **البريد الإلكتروني**
        - 📱 **WhatsApp**
        """
        if method == "print":
            return f"🖨️ Offer printed: {self.instance.title}"

        elif method == "email":
            return f"📧 Offer sent via email to clients for {self.instance.title}"

        elif method == "whatsapp":
            return f"📱 Offer sent via WhatsApp for {self.instance.title}"

        else:
            return "❌ Invalid sending method."
