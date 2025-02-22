from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات العقار إلى JSON والعكس.
    """

    formatted_price = serializers.SerializerMethodField()  # ✅ حقل مخصص لعرض السعر بصيغة منسقة
    full_description = serializers.SerializerMethodField()  # ✅ حقل مخصص لوصف العقار تفصيليًا
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات

    class Meta:
        model = Property
        fields = '__all__'  # ✅ تضمين جميع الحقول
        read_only_fields = ('id', 'created_at', 'updated_at')  # ✅ جعل الحقول الأساسية للقراءة فقط
        extra_kwargs = {
            'property_type': {'help_text': "نوع العقار (فيلا، شقة، محل تجاري، إلخ)"},
            'location': {'help_text': "الموقع الجغرافي للعقار"},
            'developer': {'help_text': "اسم المطور العقاري"},
            'description': {'help_text': "تفاصيل إضافية حول العقار"},
            'area': {'help_text': "المساحة بالمتر المربع"},
            'outdoor_area': {'help_text': "المساحة الخارجية إن وجدت"},
            'price': {'help_text': "السعر الإجمالي بالعملة المختارة (EGP أو USD)"},
            'payment_method': {'help_text': "طريقة الدفع (كاش أو أقساط)"},
            'delivery_date': {'help_text': "تاريخ تسليم العقار"},
            'maintenance_value': {'help_text': "قيمة الصيانة السنوية بالعملة المختارة"},
        }

    def get_formatted_price(self, obj):
        """
        ✅ إرجاع السعر بصيغة منسقة بناءً على العملة المختارة.
        """
        currency_symbol = "ج.م" if obj.currency == "EGP" else "$"
        return f"{currency_symbol}{obj.price:,.2f}"

    def get_full_description(self, obj):
        """
        ✅ إنشاء وصف تفصيلي للعقار يشمل أهم المعلومات.
        """
        currency_symbol = "ج.م" if obj.currency == "EGP" else "$"
        description = (
            f"Type: {obj.property_type} | Location: {obj.location} | "
            f"Area: {obj.area} sqm | Price: {currency_symbol}{obj.price:,.2f} | "
            f"Developer: {obj.developer} | Delivery: {obj.delivery_date}"
        )
        if obj.outdoor_area:
            description += f" | Outdoor Area: {obj.outdoor_area} sqm"
        return description

    def validate_price(self, value):
        """
        ✅ التحقق من أن السعر أكبر من صفر.
        """
        if value <= 0:
            raise serializers.ValidationError("💰 السعر يجب أن يكون أكبر من الصفر.")
        return value

    def validate_area(self, value):
        """
        ✅ التحقق من أن المساحة أكبر من صفر.
        """
        if value <= 0:
            raise serializers.ValidationError("📏 المساحة يجب أن تكون أكبر من الصفر.")
        return value
