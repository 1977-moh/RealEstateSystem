import uuid
import datetime
import pdfkit
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from clients.models import Client
from properties.models import Property
from employees.models import Employee


class Offer(models.Model):
    """
    ✅ نموذج يمثل العروض الترويجية الخاصة بالعقارات مع دعم العملة وإرسال الإشعارات.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ معرف فريد لكل عرض

    OFFER_TYPE_CHOICES = [
        ('Discount', 'Discount'),  # خصم
        ('Cashback', 'Cashback'),  # استرداد نقدي
        ('Exclusive', 'Exclusive Deal')  # عرض حصري
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),  # نشط
        ('Expired', 'Expired'),  # منتهي
        ('Upcoming', 'Upcoming')  # قادم
    ]

    CURRENCY_CHOICES = [
        ("EGP", "Egyptian Pound"),
        ("USD", "US Dollar"),
        ("EUR", "Euro"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Offer Title",
        help_text="أدخل عنوان العرض الترويجي."
    )

    description = models.TextField(
        verbose_name="Description",
        blank=True, null=True,
        help_text="وصف إضافي للعرض (اختياري)."
    )

    offer_type = models.CharField(
        max_length=20,
        choices=OFFER_TYPE_CHOICES,
        verbose_name="Offer Type",
        help_text="حدد نوع العرض (خصم، استرداد نقدي، عرض حصري)."
    )

    value = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Offer Value",
        help_text="قيمة العرض (كمبلغ نقدي أو نسبة مئوية)."
    )

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default="EGP",
        verbose_name="Currency"
    )

    start_date = models.DateField(
        verbose_name="Start Date",
        help_text="حدد تاريخ بدء العرض."
    )

    end_date = models.DateField(
        verbose_name="End Date",
        help_text="حدد تاريخ انتهاء العرض."
    )

    properties = models.ManyToManyField(
        Property,
        blank=True,
        verbose_name="Applicable Properties",
        help_text="حدد العقارات التي ينطبق عليها العرض."
    )

    clients = models.ManyToManyField(
        Client,
        blank=True,
        verbose_name="Applicable Clients",
        help_text="حدد العملاء المؤهلين للاستفادة من العرض."
    )

    assigned_employee = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Assigned Employee",
        help_text="الموظف المسؤول عن إدارة العرض (اختياري)."
    )

    min_purchase_amount = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.0,
        verbose_name="Minimum Purchase Amount",
        help_text="الحد الأدنى لمبلغ الشراء المؤهل لهذا العرض."
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Upcoming',
        verbose_name="Status",
        help_text="حدد حالة العرض (نشط، منتهي، قادم)."
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="تحديد ما إذا كان العرض لا يزال نشطًا أم لا."
    )

    # ✅ الحقول الزمنية
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']  # ✅ ترتيب العروض حسب الأحدث أولًا
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        """
        ✅ تحسين عرض بيانات العرض.
        """
        currency_symbol = {"EGP": "£", "USD": "$", "EUR": "€"}.get(self.currency, "")
        return f"{self.title} ({self.offer_type}) - {self.status} | {currency_symbol}{self.value:,.2f} [{self.start_date} → {self.end_date}]"

    def clean(self):
        """
        ✅ التحقق من صحة البيانات قبل الحفظ.
        """
        if self.end_date <= self.start_date:
            raise ValidationError("🚨 تاريخ انتهاء العرض يجب أن يكون بعد تاريخ البدء!")

        if self.value <= 0:
            raise ValidationError("🚨 يجب أن تكون قيمة العرض موجبة!")

        if self.min_purchase_amount < 0:
            raise ValidationError("🚨 الحد الأدنى للشراء لا يمكن أن يكون قيمة سالبة!")

        if self.status == "Active" and self.end_date < datetime.date.today():
            raise ValidationError("🚨 لا يمكن أن يكون العرض نشطًا بعد تاريخ انتهائه!")

    def is_expired(self):
        """
        ✅ التحقق مما إذا كان العرض قد انتهى.
        """
        return self.end_date < datetime.date.today()

    def calculate_discounted_price(self, property_price):
        """
        ✅ حساب السعر النهائي للعقار بعد تطبيق العرض.
        """
        if self.offer_type == "Discount":
            return max(property_price - self.value, 0)
        return property_price

    def generate_pdf_offer(self):
        """
        ✅ إنشاء ملف PDF يحتوي على تفاصيل العرض.
        """
        context = {"offer": self}
        html = render_to_string("offers/offer_template.html", context)
        pdf_path = f"media/offers/{self.id}.pdf"
        pdfkit.from_string(html, pdf_path)
        return pdf_path

    def send_email_offer(self, client_email):
        """
        ✅ إرسال العرض عبر البريد الإلكتروني.
        """
        subject = f"📢 عرض جديد: {self.title}"
        message = f"مرحبًا، لدينا عرض جديد لك!\n\n{self.description}\n💰 القيمة: {self.value} {self.currency}\n📅 متاح حتى: {self.end_date}"
        from_email = "sales@company.com"
        recipient_list = [client_email]

        send_mail(subject, message, from_email, recipient_list)

    def send_whatsapp_offer(self, client_phone):
        """
        ✅ إرسال العرض عبر واتساب مع رابط الموقع.
        """
        message = f"📢 عرض جديد: {self.title}\n🔹 التفاصيل: {self.description}\n💰 القيمة: {self.value} {self.currency}\n🌍 اكتشف المزيد: https://company-website.com/offers/{self.id}"
        whatsapp_link = f"https://wa.me/{client_phone}?text={message}"
        return whatsapp_link
