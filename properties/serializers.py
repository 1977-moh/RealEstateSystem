from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """
    Serializer لتحويل بيانات العقار إلى JSON والعكس.
    """
    formatted_price = serializers.SerializerMethodField()  # حقل مخصص لعرض السعر بصيغة منسقة
    full_description = serializers.SerializerMethodField()  # حقل مخصص لعرض وصف تفصيلي

    class Meta:
        model = Property
        fields = '__all__'  # تضمين جميع الحقول
        read_only_fields = ('created_at', 'updated_at')  # جعل الحقول الزمنية للقراءة فقط

    def get_formatted_price(self, obj):
        """
        إرجاع السعر بصيغة منسقة.
        """
        return f"${obj.price:,.2f}"

    def get_full_description(self, obj):
        """
        إنشاء وصف تفصيلي للعقار.
        """
        return (
            f"Type: {obj.property_type}, Location: {obj.location}, "
            f"Area: {obj.area} sqm, Price: ${obj.price:,.2f}"
        )

    def validate_price(self, value):
        """
        التحقق من أن السعر أكبر من صفر.
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_area(self, value):
        """
        التحقق من أن المساحة أكبر من صفر.
        """
        if value <= 0:
            raise serializers.ValidationError("Area must be greater than zero.")
        return value
