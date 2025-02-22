import uuid
import datetime
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from clients.models import Client
from properties.models import Property


class Payment(models.Model):
    """
    ✅ نموذج لتسجيل بيانات المدفوعات مع دعم العملات وحالة الدفع.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ معرف فريد لكل دفعة

    # ✅ خيارات طريقة الدفع
    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    # ✅ خيارات العملات المدعومة
    CURRENCY_CHOICES = [
        ("EGP", "Egyptian Pound"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]

    # ✅ حالة الدفع
    PAYMENT_STATUS_CHOICES = [
        ("Pending", "Pending"),  # قيد الانتظار
        ("Completed", "Completed"),  # مكتمل
        ("Failed", "Failed"),  # فشل الدفع
        ("Refunded", "Refunded"),  # مسترد
    ]

    # ✅ الحقول الأساسية
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="payments", verbose_name="Client"
    )

    property = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="payments", verbose_name="Property"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Payment Amount",
        validators=[MinValueValidator(0.01)]  # ✅ منع القيم السالبة والصفر
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="EGP",
        verbose_name="Currency"
    )

    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        verbose_name="Payment Method"
    )

    date = models.DateField(
        default=now,
        verbose_name="Payment Date"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="Pending",
        verbose_name="Payment Status"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )

    # ✅ الحقول الزمنية
    created_at = models.DateTimeField(
        default=now,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ['-date', '-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['client', 'property', 'amount', 'currency', 'date'],
                name='unique_payment_per_client_property'
            )  # ✅ منع التكرار لنفس العميل والمبلغ والعملة في نفس اليوم
        ]

    def __str__(self):
        """
        ✅ تحسين عرض البيانات في Django Admin
        """
        client_info = f" | Client: {self.client.name}" if self.client else ""
        property_info = f" | Property: {self.property.property_type} - {self.property.location}" if self.property else ""
        currency_symbol = {"EGP": "£", "USD": "$", "EUR": "€"}.get(self.currency, "")
        return f"💰 {currency_symbol}{self.amount:,.2f} {self.method} ({self.payment_status}) | {self.date.strftime('%Y-%m-%d')}{client_info}{property_info}"

    def clean(self):
        """
        ✅ التحقق من صحة البيانات قبل الحفظ:
        - يجب أن يكون المبلغ أكبر من الصفر.
        - لا يمكن أن يكون تاريخ الدفع في المستقبل.
        - منع المدفوعات المكررة لنفس العميل بنفس القيمة والعملة في نفس اليوم.
        """
        if self.amount <= 0:
            raise ValidationError("🚨 يجب أن يكون مبلغ الدفع أكبر من الصفر!")

        if self.date > datetime.date.today():
            raise ValidationError("🚨 لا يمكن أن يكون تاريخ الدفع في المستقبل!")

        existing_payment = Payment.objects.filter(
            client=self.client,
            property=self.property,
            amount=self.amount,
            currency=self.currency,
            date=self.date
        ).exclude(id=self.id).exists()

        if existing_payment:
            raise ValidationError("🚨 يوجد بالفعل دفعة بنفس المبلغ والعملة لهذا العميل في نفس اليوم!")

    def get_absolute_url(self):
        """
        ✅ إرجاع رابط URL مباشر للدفع.
        """
        return reverse("payments:payment-detail", kwargs={"pk": self.pk})

    def is_recent_payment(self):
        """
        ✅ التحقق مما إذا كانت الدفعة تمت خلال آخر 30 يومًا.
        """
        return (datetime.date.today() - self.date).days <= 30

    def is_successful_payment(self):
        """
        ✅ التحقق مما إذا كانت عملية الدفع ناجحة (مكتملة أو مستردة).
        """
        return self.payment_status in ["Completed", "Refunded"]

    @staticmethod
    def calculate_total_payments(client=None, property=None, currency="EGP"):
        """
        ✅ حساب مجموع المدفوعات حسب العميل أو العقار مع دعم العملات.
        """
        query = Payment.objects.filter(payment_status="Completed", currency=currency)
        if client:
            query = query.filter(client=client)
        if property:
            query = query.filter(property=property)
        return query.aggregate(total=models.Sum("amount"))["total"] or 0.0
