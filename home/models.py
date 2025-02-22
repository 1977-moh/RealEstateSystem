from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.urls import reverse


class SiteSettings(models.Model):
    """
    ✅ نموذج لإعدادات الموقع العامة، بحيث يكون هناك إدخال واحد فقط في قاعدة البيانات.
    """
    site_name = models.CharField(
        max_length=255,
        unique=True,  # ✅ منع تكرار اسم الموقع
        verbose_name="Site Name",
        help_text="اسم الموقع الذي سيظهر في العنوان."
    )
    logo = models.ImageField(
        upload_to='site_logo/',
        blank=True, null=True,
        verbose_name="Site Logo",
        help_text="تحميل شعار الموقع."
    )
    contact_email = models.EmailField(
        unique=True,  # ✅ التأكد من عدم تكرار البريد الإلكتروني
        verbose_name="Contact Email",
        help_text="البريد الإلكتروني الرئيسي لمراسلة العملاء."
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,  # ✅ التأكد من عدم تكرار رقم الهاتف
        verbose_name="Phone Number",
        help_text="رقم الهاتف الرئيسي لخدمة العملاء."
    )
    address = models.TextField(
        blank=True, null=True,
        verbose_name="Company Address",
        help_text="عنوان الشركة أو الموقع الرئيسي."
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def clean(self):
        """
        ✅ تقييد النموذج ليكون هناك إدخال واحد فقط في قاعدة البيانات.
        """
        if SiteSettings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("🚨 Only one SiteSettings instance is allowed!")

    def save(self, *args, **kwargs):
        """
        ✅ ضمان وجود إدخال واحد فقط عبر استدعاء `clean()` عند الحفظ.
        """
        self.clean()
        super().save(*args, **kwargs)

    def get_logo_url(self):
        """
        ✅ إرجاع رابط صورة الشعار إذا كانت موجودة، أو رابط صورة افتراضية.
        """
        return self.logo.url if self.logo else "/static/images/default-logo.png"

    def get_absolute_url(self):
        """
        ✅ إرجاع رابط URL مباشر لإعدادات الموقع.
        """
        return reverse("site-settings-detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_settings():
        """
        ✅ استرجاع إعدادات الموقع أو إنشاء إدخال جديد إذا لم يكن موجودًا.
        """
        return SiteSettings.objects.first() or SiteSettings.objects.create(
            site_name="Default Site",
            contact_email="admin@company.com",
            phone_number="+201234567890"
        )

    def __str__(self):
        return f"{self.site_name} - {self.contact_email} | {self.phone_number}"
