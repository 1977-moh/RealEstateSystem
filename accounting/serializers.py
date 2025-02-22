from rest_framework import serializers
from .models import Salary, Bonus, Deduction, SalesCommission


class SalarySerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لنموذج المرتب مع دعم العملة وحساب إجمالي الراتب تلقائيًا.
    """
    computed_salary = serializers.SerializerMethodField()  # ✅ حساب الراتب بعد الضرائب
    total_salary_with_commission = serializers.SerializerMethodField()  # ✅ حساب إجمالي الراتب شاملاً العمولات
    currency = serializers.ChoiceField(choices=[("EGP", "Egyptian Pound"), ("USD", "US Dollar")], default="EGP")

    class Meta:
        model = Salary
        fields = '__all__'
        read_only_fields = ('computed_salary', 'total_salary_with_commission', 'created_at', 'updated_at')

    def get_computed_salary(self, obj):
        """
        ✅ حساب الراتب الصافي بعد الضرائب.
        """
        tax_amount = (obj.tax_deduction / 100) * obj.base_salary
        return obj.base_salary - tax_amount

    def get_total_salary_with_commission(self, obj):
        """
        ✅ حساب الراتب الكلي شاملاً العمولات والمكافآت والخصومات.
        """
        commission = sum(commission.sales_amount * (obj.commission_rate / 100) for commission in obj.employee.commissions.all())
        total_salary = obj.base_salary + obj.bonus + commission - obj.deductions
        return self.convert_currency(total_salary, obj.currency)

    def convert_currency(self, amount, currency):
        """
        ✅ تحويل الراتب بين العملات عند الحاجة.
        """
        exchange_rate = 30 if currency == "EGP" else 1  # ✅ افتراض أن 1 USD = 30 EGP
        return f"{amount * exchange_rate:.2f} {currency}"


class BonusSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لنموذج المكافآت مع دعم العملة.
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    currency = serializers.CharField(source="employee.salary.currency", read_only=True)

    class Meta:
        model = Bonus
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_formatted_amount(self, obj):
        """
        ✅ عرض المكافأة مع دعم العملة.
        """
        return f"{obj.amount:.2f} {obj.employee.salary.currency}"


class DeductionSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لنموذج الخصومات مع دعم العملة.
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    formatted_amount = serializers.SerializerMethodField()
    currency = serializers.CharField(source="employee.salary.currency", read_only=True)

    class Meta:
        model = Deduction
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_formatted_amount(self, obj):
        """
        ✅ عرض الخصم مع دعم العملة.
        """
        return f"{obj.amount:.2f} {obj.employee.salary.currency}"


class SalesCommissionSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لنموذج العمولات مع حسابها تلقائيًا ودعم العملة.
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    formatted_sales = serializers.SerializerMethodField()
    computed_commission = serializers.SerializerMethodField()
    currency = serializers.CharField(source="employee.salary.currency", read_only=True)

    class Meta:
        model = SalesCommission
        fields = '__all__'
        read_only_fields = ('computed_commission', 'created_at', 'updated_at')

    def get_formatted_sales(self, obj):
        """
        ✅ عرض المبيعات بطريقة محسنة.
        """
        return f"{obj.sales_amount:.2f} {obj.employee.salary.currency}"

    def get_computed_commission(self, obj):
        """
        ✅ حساب العمولة تلقائيًا بناءً على `sales_amount` و `commission_rate` من `Salary`.
        """
        salary = obj.employee.salary
        if salary:
            commission_rate = salary.commission_rate / 100
            commission_value = obj.sales_amount * commission_rate
            return f"{commission_value:.2f} {salary.currency}"
        return "0.00"

    def validate_sales_amount(self, value):
        """
        ✅ التحقق من أن قيمة المبيعات موجبة.
        """
        if value <= 0:
            raise serializers.ValidationError("🚨 Sales amount must be greater than zero.")
        return value
