import uuid
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from datetime import date
from django.apps import apps  # ✅ لمنع مشاكل الاستيراد الدائري


class Property(models.Model):
    """
    ✅ نموذج يمثل العقارات داخل النظام العقاري.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ✅ خيارات نوع العقار
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

    # ✅ خيارات طريقة السداد
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Installment', 'Installment'),
    ]

    # ✅ خيارات نوع قيمة الصيانة
    MAINTENANCE_VALUE_TYPE_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed', 'Fixed'),
    ]

    # ✅ الحقول الأساسية
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES, verbose_name="Property Type")
    location = models.CharField(max_length=255, verbose_name="Location")
    developer = models.CharField(max_length=255, verbose_name="Developer")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Property Slug")
    description = models.TextField(blank=True, null=True, verbose_name="Property Description")

    area = models.FloatField(verbose_name="Area (sqm)", help_text="المساحة بالمتر المربع")
    outdoor_area = models.FloatField(blank=True, null=True, verbose_name="Outdoor Area (sqm)")

    price = models.DecimalField(
        max_digits=15, decimal_places=2,
        verbose_name="Price",
        help_text="السعر الإجمالي للعقار",
        validators=[MinValueValidator(0)]
    )

    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment Method")
    delivery_method = models.TextField(verbose_name="Delivery Method")

    delivery_date = models.DateField(
        verbose_name="Delivery Date",
        help_text="تاريخ تسليم العقار",
    )

    payment_percentage_for_delivery = models.FloatField(
        verbose_name="Payment Percentage for Delivery (%)",
        help_text="النسبة المطلوبة من السعر عند التسليم",
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    maintenance_value_type = models.CharField(
        max_length=20, choices=MAINTENANCE_VALUE_TYPE_CHOICES,
        verbose_name="Maintenance Value Type"
    )

    maintenance_value = models.DecimalField(
        max_digits=15, decimal_places=2,
        verbose_name="Maintenance Value",
        help_text="قيمة الصيانة المطلوبة",
        validators=[MinValueValidator(0)]
    )

    is_sold = models.BooleanField(default=False, verbose_name="Sold Status")

    # ✅ الطوابع الزمنية
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        ✅ توليد `slug` تلقائيًا من `property_type` + `location` + `developer`
        مع التأكد من تفرده.
        """
        if not self.slug:
            base_slug = slugify(f"{self.property_type}-{self.location}-{self.developer}")
            unique_slug = base_slug
            counter = 1
            while Property.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        # ✅ التحقق من صحة تاريخ التسليم
        self.validate_delivery_date()

        super().save(*args, **kwargs)

    def validate_delivery_date(self):
        """✅ منع حفظ تاريخ تسليم في الماضي"""
        if self.delivery_date < date.today():
            raise ValueError("❌ The delivery date cannot be in the past.")

    def get_absolute_url(self):
        """
        ✅ إرجاع رابط URL مباشر للعقار.
        """
        return reverse("properties:property-detail", kwargs={"slug": self.slug})

    def calculate_maintenance_cost(self):
        """
        ✅ حساب تكلفة الصيانة بناءً على نوعها:
        - إذا كانت `Fixed` يتم استخدام القيمة كما هي.
        - إذا كانت `Percentage` يتم احتسابها كنسبة مئوية من سعر العقار.
        """
        return self.maintenance_value if self.maintenance_value_type == "Fixed" else (
            (self.price * self.maintenance_value) / 100 if self.maintenance_value_type == "Percentage" else 0
        )

    def get_payment_on_delivery(self):
        """
        ✅ حساب المبلغ المستحق عند التسليم بناءً على النسبة المحددة.
        """
        return (self.price * self.payment_percentage_for_delivery) / 100

    def is_available(self):
        """
        ✅ التحقق مما إذا كان العقار متاحًا للبيع.
        """
        return not self.is_sold

    def __str__(self):
        """
        ✅ تحسين طريقة عرض العقار عند استدعائه كنص.
        """
        availability = "Sold" if self.is_sold else "Available"
        return f"{self.property_type} | {self.location} | ${self.price} | {availability}"
