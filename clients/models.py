import uuid
import random
from datetime import timedelta, date
from django.db import models
from django.utils.timezone import now
from django.utils.text import slugify
from django.core.validators import EmailValidator
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    """
    ✅ نموذج يمثل العملاء العقاريين الذكيين مع الذكاء الاصطناعي والتحليلات المتقدمة.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # ✅ البيانات الأساسية
    name = models.CharField(max_length=255, verbose_name="Client Name")
    slug = models.SlugField(unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="Email Address", validators=[EmailValidator()])
    phone = PhoneNumberField(blank=True, null=True, verbose_name="Phone Number")

    address = models.TextField(blank=True, null=True, verbose_name="Address")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Location")
    interests = models.TextField(blank=True, null=True, verbose_name="Interests")
    client_request_details = models.TextField(blank=True, null=True, verbose_name="Request Details")

    # ✅ مصادر العملاء
    CLIENT_SOURCES = [
        ('advertisement', 'Advertisement'),
        ('referral', 'Referral'),
        ('website', 'Website Inquiry'),
        ('social_media', 'Social Media'),
        ('direct_contact', 'Direct Contact'),
        ('other', 'Other'),
    ]
    client_source = models.CharField(
        max_length=50, choices=CLIENT_SOURCES, default='other', verbose_name="Client Source"
    )

    # ✅ حالة العميل
    STATUS_CHOICES = [
        ('potential', 'Potential'),
        ('active', 'Active'),
        ('previous', 'Previous Client'),
        ('vip', 'VIP'),
        ('interested', 'Interested'),
        ('repeated_buyer', 'Repeated Buyer'),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='potential', verbose_name="Client Status"
    )

    # ✅ إعدادات الذكاء الاصطناعي والتحليل
    predicted_interest_score = models.FloatField(default=0.0, verbose_name="Predicted Interest Score")
    last_interaction = models.DateField(default=now, verbose_name="Last Interaction Date")
    follow_up_date = models.DateField(blank=True, null=True, verbose_name="Next Follow-Up Date")

    # ✅ الحقول الزمنية
    entry_date = models.DateTimeField(auto_now_add=True, verbose_name="Entry Date")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        constraints = [
            models.UniqueConstraint(fields=['email', 'client_source'], name='unique_client_per_source')
        ]

    def save(self, *args, **kwargs):
        """
        ✅ تحديث حالة العميل بناءً على التفاعلات والذكاء الاصطناعي.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()

        # ✅ تحديث توقع اهتمام العميل بناءً على البيانات المتوفرة
        self.predicted_interest_score = self.calculate_client_value()

        # ✅ تحديث موعد المتابعة التلقائي
        self.update_follow_up_date()

        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """✅ إنشاء `slug` فريد بناءً على اسم العميل"""
        base_slug = slugify(self.name)
        unique_slug = base_slug
        counter = 1
        while Client.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        return unique_slug

    def calculate_client_value(self):
        """✅ تقييم العميل بناءً على اهتماماته والطلبات السابقة"""
        value = 0

        if self.interests:
            interests = self.interests.lower()
            if "luxury" in interests:
                value += 5000
            if "apartment" in interests:
                value += 3000
            if "villa" in interests:
                value += 7000

        if self.client_request_details:
            value += len(self.client_request_details.split()) * 10  # زيادة التقييم بناءً على عدد الكلمات

        return value + random.uniform(0, 20)

    def update_follow_up_date(self):
        """✅ تحديث موعد المتابعة بناءً على حالة العميل"""
        if self.status == 'potential' and not self.follow_up_date:
            self.follow_up_date = date.today() + timedelta(days=30)
        elif self.status == 'previous' and not self.follow_up_date:
            self.follow_up_date = date.today() + timedelta(days=90)

    def get_absolute_url(self):
        """✅ إنشاء رابط لملف العميل"""
        return reverse("client_detail", kwargs={"slug": self.slug})

    def __str__(self):
        """✅ تحسين طريقة عرض `Client`"""
        return f"{self.name} | {self.email} | {self.get_client_source_display()} | {self.get_status_display()}"
