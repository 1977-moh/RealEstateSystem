from django.db import models
from django.utils.timezone import now


class Property(models.Model):
    """
    نموذج لتمثيل العقارات داخل النظام.
    """

    # خيارات نوع العقار
    PROPERTY_TYPE_CHOICES = [
        ('Standalone Villa', 'Standalone Villa'),
        ('Twin Villa', 'Twin Villa'),
        ('Town Villa', 'Town Villa'),
        ('Duplex', 'Duplex'),
        ('Penthouse', 'Penthouse'),
        ('Apartment', 'Apartment'),
        ('Shop', 'Shop'),
        ('Office', 'Office'),
        ('Clinic', 'Clinic'),
    ]

    # خيارات طريقة السداد
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Installment', 'Installment'),
    ]

    # خيارات نوع قيمة الصيانة
    MAINTENANCE_VALUE_TYPE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]

    # الحقول الأساسية
    property_type = models.CharField(
        max_length=50,
        choices=PROPERTY_TYPE_CHOICES,
        verbose_name="Property Type"
    )
    location = models.CharField(max_length=255, verbose_name="Location")
    developer = models.CharField(max_length=255, verbose_name="Developer")
    description = models.TextField(blank=True, null=True, verbose_name="Property Description")
    area = models.FloatField(verbose_name="Area (sqm)")
    outdoor_area = models.FloatField(blank=True, null=True, verbose_name="Outdoor Area (sqm)")
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Price")
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Payment Method"
    )
    delivery_method = models.TextField(verbose_name="Delivery Method")
    delivery_date = models.DateField(verbose_name="Delivery Date")
    payment_percentage_for_delivery = models.FloatField(
        verbose_name="Payment Percentage for Delivery (%)"
    )
    maintenance_value_type = models.CharField(
        max_length=20,
        choices=MAINTENANCE_VALUE_TYPE_CHOICES,
        verbose_name="Maintenance Value Type"
    )
    maintenance_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Maintenance Value"
    )

    # الطوابع الزمنية
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']  # ترتيب السجلات افتراضيًا حسب الأحدث

    def __str__(self):
        """
        عرض تفاصيل العقار عند استدعائه كنص.
        """
        return f"{self.property_type} at {self.location} - {self.price} USD"
