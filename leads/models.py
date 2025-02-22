import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError


class Lead(models.Model):
    """
    ✅ نموذج العملاء المتوقعين (Leads) في النظام العقاري.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )  # ✅ معرف فريد لكل `Lead`

    campaign = models.ForeignKey(
        "campaigns.Campaign",
        on_delete=models.CASCADE,
        related_name="leads",
        verbose_name="Related Campaign",
        help_text="الحملة الإعلانية التي تم الحصول على العميل المحتمل من خلالها."
    )

    name = models.CharField(
        max_length=255,
        verbose_name="Lead Name",
        help_text="أدخل اسم العميل المحتمل."
    )

    email = models.EmailField(
        verbose_name="Email",
        help_text="أدخل بريدًا إلكترونيًا صالحًا.",
        validators=[EmailValidator(message="❌ البريد الإلكتروني غير صالح.")]
    )

    phone = models.CharField(
        max_length=20,
        blank=True, null=True,
        verbose_name="Phone",
        help_text="أدخل رقم هاتف صالح (اختياري).",
        validators=[RegexValidator(regex=r'^\+?\d{7,15}$', message="❌ رقم الهاتف غير صالح. يجب أن يكون بين 7 و 15 رقمًا.")]
    )

    assigned_to = models.ForeignKey(
        "employees.Employee",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Assigned Employee",
        help_text="الموظف المسؤول عن متابعة هذا العميل المحتمل (اختياري)."
    )

    STATUS_CHOICES = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("Closed", "Closed"),
        ("Converted", "Converted"),  # ✅ تم تحويل العميل إلى صفقة ناجحة
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status",
        help_text="حدد حالة العميل المحتمل (جديد - قيد المتابعة - مغلق - تم التحويل)."
    )

    created_at = models.DateTimeField(
        default=now,
        verbose_name="Created At",
        help_text="وقت تسجيل العميل المحتمل."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
        help_text="آخر تعديل لسجل العميل المحتمل."
    )

    class Meta:
        ordering = ['-created_at']  # ✅ ترتيب العملاء المتوقعين حسب الأحدث
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        constraints = [
            models.UniqueConstraint(fields=['email', 'campaign'], name='unique_lead_per_campaign')
        ]  # ✅ منع تسجيل نفس العميل في نفس الحملة أكثر من مرة

    def clean(self):
        """
        ✅ التحقق من صحة البيانات قبل الحفظ:
        - التأكد من عدم تكرار البريد الإلكتروني حتى لو كان بأحرف مختلفة.
        - التأكد من أن العميل غير مكرر في حملة أخرى.
        """
        self.email = self.email.lower().strip()

        # ✅ التحقق من البريد الإلكتروني عبر الحملات
        existing_lead = Lead.objects.filter(email=self.email, campaign=self.campaign).exclude(pk=self.pk).exists()
        if existing_lead:
            raise ValidationError("❌ هذا البريد الإلكتروني مسجل بالفعل في هذه الحملة!")

        # ✅ التأكد من أن العميل غير مكرر في حملات مختلفة
        multiple_campaigns = Lead.objects.filter(email=self.email).exclude(campaign=self.campaign).count()
        if multiple_campaigns >= 3:  # 🔍 السماح بحد أقصى 3 حملات لكل بريد إلكتروني
            raise ValidationError("❌ لا يمكن تسجيل هذا البريد الإلكتروني في أكثر من 3 حملات!")

    def save(self, *args, **kwargs):
        """
        ✅ تعديل آلي على البيانات قبل الحفظ:
        - تحويل البريد الإلكتروني إلى **أحرف صغيرة** لتجنب التكرار بحالات مختلفة.
        - إزالة **المسافات الزائدة** من الاسم.
        - التأكد من أن رقم الهاتف **يتم حفظه بدون مسافات**.
        """
        self.email = self.email.lower().strip()
        self.name = " ".join(self.name.split())

        if self.phone:
            self.phone = self.phone.replace(" ", "").strip()

        super().save(*args, **kwargs)

    def __str__(self):
        """✅ تحسين طريقة عرض `Lead` لضمان عدم حدوث خطأ عند عدم وجود حملة."""
        campaign_name = self.campaign.name if self.campaign else "No Campaign"
        return f"{self.name} ({self.email}) - {self.status} [{campaign_name}]"
