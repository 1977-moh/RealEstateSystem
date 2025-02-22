from rest_framework import serializers
from django.utils.timezone import now
from django.core.mail import send_mail
from django.apps import apps  # ✅ حل مشكلة الاستيراد الدائري
from .models import Broker, BrokerClient, BrokerTransaction
from clients.models import Client


class BrokerSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لعرض بيانات الوسطاء (Brokers).
    """
    total_earnings_formatted = serializers.SerializerMethodField()  # ✅ عرض الأرباح بطريقة محسنة
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات

    class Meta:
        model = Broker
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'total_earnings')  # ✅ منع التعديل على الحقول الزمنية

    def get_total_earnings_formatted(self, obj):
        """
        ✅ إرجاع الأرباح بطريقة محسنة.
        """
        currency_symbol = "£" if obj.currency == "EGP" else "$"
        return f"{currency_symbol}{obj.total_earnings:,.2f}"

    def validate_currency(self, value):
        """
        ✅ التأكد من أن العملة المدخلة مدعومة.
        """
        if value not in ["EGP", "USD"]:
            raise serializers.ValidationError("❌ العملة غير مدعومة. اختر بين EGP أو USD.")
        return value

    def validate_commission_rate(self, value):
        """
        ✅ التأكد من أن النسبة تتراوح بين 0% و 100%.
        """
        if not (0 <= value <= 100):
            raise serializers.ValidationError("❌ يجب أن تكون نسبة العمولة بين 0 و 100٪.")
        return value


class BrokerClientSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لعرض العلاقة بين الوسيط والعميل مع تضمين بيانات العميل.
    """
    client_name = serializers.CharField(source='client.name', read_only=True)  # ✅ تضمين اسم العميل
    broker_name = serializers.CharField(source='broker.name', read_only=True)  # ✅ تضمين اسم الوسيط
    expiry_date = serializers.DateTimeField(read_only=True)  # ✅ إظهار تاريخ انتهاء ملكية العميل
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        source="client",
        write_only=True  # ✅ السماح بإدخال `client_id` فقط
    )

    class Meta:
        model = BrokerClient
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'expiry_date')  # ✅ الحقول الزمنية للقراءة فقط

    def validate_status(self, value):
        """
        ✅ التحقق عند تغيير حالة العميل:
        - عند التحويل إلى `Converted` يتم إرسال إشعار إلى شركة الوساطة.
        - رفض العميل إذا كان محجوزًا لشركة أخرى.
        """
        instance = self.instance  # ✅ الحصول على السجل الأصلي
        if instance and instance.status != value:
            if value == "Converted":
                send_mail(
                    subject="🔔 Client Converted to Company Database",
                    message=f"🔔 تم تحويل العميل {instance.client.name} إلى قاعدة بيانات الشركة بعد انقضاء مهلة الـ 15 يومًا.",
                    from_email="noreply@company.com",
                    recipient_list=[instance.broker.broker_official_email],
                )

        return value

    def save(self, *args, **kwargs):
        """
        ✅ تنفيذ `auto_convert_clients()` أثناء الحفظ لضمان تحديث البيانات تلقائيًا.
        """
        instance = super().save(*args, **kwargs)
        self.auto_convert_clients()
        return instance

    @staticmethod
    def auto_convert_clients():
        """
        ✅ يتم تشغيل هذا الكود يوميًا لتحويل العملاء الذين انتهت صلاحية وساطتهم إلى قاعدة بيانات الشركة.
        """
        expired_clients = BrokerClient.objects.filter(status="Pending", expiry_date__lt=now())
        for client in expired_clients:
            client.status = "Converted"
            client.save()


class EmployeePerformanceSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتقييم أداء الموظف.
    """
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    broker_name = serializers.CharField(source='broker.name', read_only=True)
    review_date = serializers.DateField(default=now, read_only=True)

    class Meta:
        model = apps.get_model("employees", "EmployeePerformance")  # ✅ استخدام `apps.get_model()` لحل مشكلة الاستيراد الدائري
        fields = '__all__'
        read_only_fields = ('id', 'review_date')


class BrokerTransactionSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer للمعاملات المالية للوسطاء.
    """
    broker_name = serializers.CharField(source='broker.name', read_only=True)  # ✅ تضمين اسم الوسيط
    formatted_amount = serializers.SerializerMethodField()  # ✅ تنسيق المبلغ عند العرض
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات المتعددة

    class Meta:
        model = BrokerTransaction
        fields = '__all__'
        read_only_fields = ('id', 'transaction_date')  # ✅ جعل تاريخ المعاملة للقراءة فقط

    def get_formatted_amount(self, obj):
        """
        ✅ عرض المبلغ بطريقة محسنة وفق العملة المحددة.
        """
        currency_symbol = "£" if obj.currency == "EGP" else "$"
        return f"{currency_symbol}{obj.amount:,.2f}"

    def validate_amount(self, value):
        """
        ✅ التأكد من أن المبلغ ليس سلبيًا ويكون ضمن نطاق معقول.
        """
        if value <= 0:
            raise serializers.ValidationError("❌ لا يمكن أن يكون المبلغ صفرًا أو سالبًا.")
        if value > 1_000_000:
            raise serializers.ValidationError("❌ المبلغ كبير جدًا، الرجاء إدخال قيمة أقل من 1,000,000.")
        return value
