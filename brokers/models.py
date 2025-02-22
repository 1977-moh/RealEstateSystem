import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import EmailValidator
from django.apps import apps  # ✅ حل مشكلة الاستيراد الدائري


class Broker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Broker Name")
    broker_official_email = models.EmailField(
        unique=True,
        verbose_name="Broker Official Email",
        validators=[EmailValidator(message="❌ البريد الإلكتروني غير صالح.")]
    )
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    email = models.EmailField(unique=True, verbose_name="Email")
    currency = models.CharField(
        max_length=3,
        choices=[("EGP", "EGP"), ("USD", "USD")],
        default="EGP",
        verbose_name="Currency"
    )

    responsible_employee = models.ForeignKey(
        "employees.Employee", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_brokers", verbose_name="Responsible Employee"
    )

    commission_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0, verbose_name="Commission Rate (%)"
    )
    additional_incentives = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Additional Incentives"
    )
    total_earnings = models.DecimalField(
        max_digits=15, decimal_places=2, default=0.0, verbose_name="Total Earnings"
    )

    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Broker"
        verbose_name_plural = "Brokers"

    def __str__(self):
        return f"{self.name} ({self.email})"

    def calculate_total_earnings(self):
        """
        ✅ تحديث إجمالي الأرباح تلقائيًا عند أي تغيير.
        """
        total_transactions = self.financial_transactions.aggregate(models.Sum("amount"))["amount__sum"] or 0
        self.total_earnings = total_transactions + self.additional_incentives
        self.save()


class BrokerClient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    broker = models.ForeignKey(
        Broker, on_delete=models.CASCADE, related_name="broker_clients", verbose_name="Broker"
    )
    client = models.ForeignKey(
        "clients.Client", on_delete=models.CASCADE, related_name="broker_clients", verbose_name="Client"
    )

    property_value = models.DecimalField(
        max_digits=15, decimal_places=2, verbose_name="Property Value"
    )

    commission_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Commission Amount"
    )

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Completed", "Completed"),
        ("Converted", "Converted"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending",
        verbose_name="Status"
    )

    assigned_date = models.DateTimeField(default=now, verbose_name="Assigned Date")
    expiry_date = models.DateTimeField(null=True, blank=True, verbose_name="Expiry Date")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Broker Client"
        verbose_name_plural = "Broker Clients"

    def __str__(self):
        return f"Client: {self.client.name} | Broker: {self.broker.name} | Status: {self.status}"

    def save(self, *args, **kwargs):
        """
        ✅ حل مشكلة الاستيراد الدائري باستخدام `apps.get_model()` فقط عند الحاجة.
        """
        super().save(*args, **kwargs)

        if self.status == "Converted" and self.broker.responsible_employee:
            # ✅ استخدام `apps.get_model()` لتجنب الاستيراد الدائري
            EmployeePerformance = apps.get_model("employees", "EmployeePerformance")
            employee_performance, created = EmployeePerformance.objects.get_or_create(
                employee=self.broker.responsible_employee
            )
            employee_performance.update_performance()


class BrokerTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    broker = models.ForeignKey(
        Broker, on_delete=models.CASCADE, related_name="financial_transactions", verbose_name="Broker"
    )

    TRANSACTION_TYPES = [
        ("Commission", "Commission"),
        ("Bonus", "Bonus"),
        ("Other", "Other"),
    ]

    transaction_type = models.CharField(
        max_length=50,
        choices=TRANSACTION_TYPES,
        verbose_name="Transaction Type"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    currency = models.CharField(
        max_length=3,
        choices=[("EGP", "EGP"), ("USD", "USD")],
        default="EGP",
        verbose_name="Currency"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    transaction_date = models.DateTimeField(default=now, verbose_name="Transaction Date")

    class Meta:
        ordering = ["-transaction_date"]
        verbose_name = "Broker Transaction"
        verbose_name_plural = "Broker Transactions"

    def __str__(self):
        return f"{self.transaction_type} - {self.broker.name} (${self.amount})"

    def save(self, *args, **kwargs):
        """
        ✅ تحديث أرباح الوسيط عند إضافة معاملة مالية جديدة.
        """
        super().save(*args, **kwargs)
        self.broker.calculate_total_earnings()
