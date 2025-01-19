from rest_framework import serializers
from .models import Employee
from datetime import date


class EmployeeSerializer(serializers.ModelSerializer):
    years_of_service = serializers.SerializerMethodField()  # حقل مخصص لحساب عدد سنوات الخدمة

    class Meta:
        model = Employee
        fields = '__all__'  # تضمين جميع الحقول بالإضافة إلى الحقول المخصصة

    def validate_email(self, value):
        """
        التحقق من صحة البريد الإلكتروني.
        """
        if "@" not in value or "." not in value:
            raise serializers.ValidationError("Please enter a valid email address.")
        return value

    def validate_phone(self, value):
        """
        التحقق من صحة رقم الهاتف (يجب أن يحتوي على أرقام فقط).
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def get_years_of_service(self, obj):
        """
        حساب عدد سنوات الخدمة بناءً على تاريخ التوظيف.
        """
        if obj.hire_date:
            return date.today().year - obj.hire_date.year
        return 0
