import re
from rest_framework import serializers
from django.apps import apps  # ✅ حل مشكلة الاستيراد الدائري
from .models import Employee, Department, JobTitle, Salary, LeaveRequest, PerformanceReview
from datetime import date


class DepartmentSerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة أقسام الشركة."""
    class Meta:
        model = Department
        fields = '__all__'


class JobTitleSerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة المسميات الوظيفية."""
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = JobTitle
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    """✅ Serializer لتحويل بيانات الموظف إلى JSON والعكس."""
    years_of_service = serializers.SerializerMethodField(read_only=True)
    age = serializers.SerializerMethodField(read_only=True)
    department = DepartmentSerializer(read_only=True)
    job_title = JobTitleSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_email(self, value):
        """✅ التحقق من صحة البريد الإلكتروني."""
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            raise serializers.ValidationError("📧 الرجاء إدخال بريد إلكتروني صالح.")

        if not value.endswith("@company.com"):
            raise serializers.ValidationError("📧 البريد الإلكتروني يجب أن يكون ضمن نطاق الشركة (@company.com).")

        return value

    def validate_phone(self, value):
        """✅ التحقق من صحة رقم الهاتف."""
        if not re.match(r"^\+?\d{7,15}$", value):
            raise serializers.ValidationError("📞 رقم الهاتف يجب أن يحتوي فقط على أرقام ويمكن أن يبدأ بـ '+'.")
        return value

    def get_years_of_service(self, obj):
        """✅ حساب عدد سنوات الخدمة."""
        if obj.hire_date:
            today = date.today()
            delta = today.year - obj.hire_date.year
            if today < obj.hire_date.replace(year=today.year):
                delta -= 1
            return "< 1 year" if delta == 0 else f"{delta} years"
        return "< 1 year"

    def get_age(self, obj):
        """✅ حساب عمر الموظف."""
        if obj.birth_date:
            today = date.today()
            return today.year - obj.birth_date.year - ((today.month, today.day) < (obj.birth_date.month, obj.birth_date.day))
        return None


class SalarySerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة رواتب الموظفين."""
    employee = EmployeeSerializer(read_only=True)
    total_salary = serializers.SerializerMethodField(read_only=True)
    commission_earned = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Salary
        fields = '__all__'

    def validate_base_salary(self, value):
        """✅ التحقق من أن الراتب الأساسي لا يمكن أن يكون سالبًا."""
        if value < 0:
            raise serializers.ValidationError("💰 الراتب الأساسي لا يمكن أن يكون رقمًا سالبًا.")
        return value

    def get_total_salary(self, obj):
        """✅ حساب صافي الراتب بعد الضرائب والخصومات والمكافآت والعمولات."""
        SalesCommission = apps.get_model("employees", "SalesCommission")  # ✅ جلب النموذج لتجنب الاستيراد الدائري
        tax_amount = (obj.tax_deduction / 100) * obj.base_salary
        commission = sum(comm.commission_earned or 0 for comm in SalesCommission.objects.filter(employee=obj.employee))
        return obj.base_salary + obj.bonus + commission - obj.deductions - tax_amount

    def get_commission_earned(self, obj):
        """✅ حساب إجمالي العمولات المكتسبة من مبيعات الموظف."""
        SalesCommission = apps.get_model("employees", "SalesCommission")  # ✅ جلب النموذج فقط عند الحاجة
        return sum(comm.commission_earned or 0 for comm in SalesCommission.objects.filter(employee=obj.employee))


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة تقييم أداء الموظف."""
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = PerformanceReview
        fields = '__all__'


class LeaveRequestSerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة طلبات الإجازات."""
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = '__all__'

    def validate(self, data):
        """✅ التحقق من أن تاريخ نهاية الإجازة لا يمكن أن يكون قبل تاريخ بدايتها."""
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("⏳ تاريخ نهاية الإجازة لا يمكن أن يكون قبل تاريخ بدايتها.")
        return data


class SalesCommissionSerializer(serializers.ModelSerializer):
    """✅ Serializer لإدارة العمولات وحسابها بناءً على المبيعات."""
    employee = EmployeeSerializer(read_only=True)
    commission_earned = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model("employees", "SalesCommission")  # ✅ حل مشكلة الاستيراد
        fields = '__all__'

    def get_commission_earned(self, obj):
        """✅ حساب العمولة بناءً على نسبة العمولة أو العمولة الثابتة لكل مليون."""
        Salary = apps.get_model("employees", "Salary")  # ✅ جلب النموذج عند الحاجة
        salary = Salary.objects.filter(employee=obj.employee).first()
        if salary:
            if salary.commission_rate:
                return obj.sales_amount * (salary.commission_rate / 100)
            elif salary.commission_fixed:
                return (obj.sales_amount / 1_000_000) * salary.commission_fixed
        return 0.0
