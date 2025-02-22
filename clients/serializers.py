from rest_framework import serializers
from .models import Client
from datetime import date
import phonenumbers

class ClientSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات Client إلى JSON والعكس.
    """
    days_since_entry = serializers.SerializerMethodField(help_text="📅 عدد الأيام منذ إدخال العميل إلى النظام.")
    status_display = serializers.SerializerMethodField(help_text="📌 الوصف الكامل لحالة العميل.")
    currency = serializers.ChoiceField(
        choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP",
        help_text="💰 اختر العملة المناسبة (EGP أو USD)."
    )  # ✅ دعم العملات

    class Meta:
        model = Client
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'entry_date')  # ✅ جعل `id` للقراءة فقط

    def validate_phone(self, value):
        """
        ✅ التحقق من أن رقم الهاتف صالح وفقًا للمعايير الدولية.
        """
        if value:
            try:
                parsed_number = phonenumbers.parse(value, None)
                if not phonenumbers.is_valid_number(parsed_number):
                    raise serializers.ValidationError("❌ رقم الهاتف غير صالح وفقًا للمعايير الدولية.")
            except phonenumbers.NumberParseException:
                raise serializers.ValidationError("❌ تنسيق رقم الهاتف غير صحيح.")
        return value

    def get_days_since_entry(self, obj):
        """
        ✅ إرجاع عدد الأيام منذ إدخال العميل إلى النظام، مع التحقق من القيم الفارغة.
        """
        if obj.entry_date:
            return (date.today() - obj.entry_date.date()).days
        return None

    def get_status_display(self, obj):
        """
        ✅ إرجاع النص الكامل لحالة العميل.
        """
        return obj.get_status_display()
