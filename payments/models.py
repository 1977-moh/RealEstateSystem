from django.db import models

class Payment(models.Model):
    """
    نموذج لتسجيل بيانات المدفوعات.
    """
    # خيارات طريقة الدفع
    PAYMENT_METHODS = [
        ("Cash", "Cash"),
        ("Credit Card", "Credit Card"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    # الحقول
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Payment Amount"
    )
    method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        verbose_name="Payment Method"
    )
    date = models.DateField(verbose_name="Payment Date")
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At"
    )

    class Meta:
        verbose_name = "Payment"  # اسم النموذج المفرد
        verbose_name_plural = "Payments"  # اسم النموذج الجمع
        ordering = ['-date']  # ترتيب المدفوعات حسب الأحدث

    def __str__(self):
        return f"{self.amount} - {self.method} on {self.date}"
