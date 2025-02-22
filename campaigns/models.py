import uuid
import requests
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from datetime import date
from django.apps import apps  # ✅ استيراد التطبيقات لتجنب المشكلة الدائرية


class Campaign(models.Model):
    """
    ✅ نموذج يمثل الحملات الإعلانية على المنصات المختلفة.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Campaign Name")
    platform = models.CharField(
        max_length=50,
        choices=[
            ("Facebook", "Facebook"),
            ("Google", "Google Ads"),
            ("TikTok", "TikTok Ads"),
            ("Instagram", "Instagram"),
            ("LinkedIn", "LinkedIn"),
        ],
        verbose_name="Advertising Platform"
    )

    budget = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Budget",
        validators=[MinValueValidator(1)]
    )

    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")

    total_spent = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.0,
        verbose_name="Total Spent",
    )

    revenue_generated = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0.0,
        verbose_name="Revenue Generated",
    )

    leads_acquired = models.PositiveIntegerField(default=0, verbose_name="Leads Acquired")

    status = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Paused", "Paused"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Active",
        verbose_name="Status"
    )

    campaign_url = models.URLField(blank=True, null=True, verbose_name="Campaign API URL")

    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def clean(self):
        """✅ التحقق من صحة تاريخ البداية والنهاية"""
        if self.start_date < date.today():
            raise ValidationError("❌ The start date cannot be in the past.")

        if self.end_date < self.start_date:
            raise ValidationError("❌ The end date must be after the start date.")

    @property
    def daily_budget(self):
        total_days = max((self.end_date - self.start_date).days, 1)
        return round(self.budget / total_days, 2)

    @property
    def remaining_budget(self):
        return max(self.budget - self.total_spent, 0)

    @property
    def calculate_roi(self):
        if self.total_spent == 0:
            return 0
        return round(((self.revenue_generated - self.total_spent) / self.total_spent) * 100, 2)

    def sync_campaign_data(self):
        """
        ✅ مزامنة بيانات الحملة من API خارجي وتحميل الـ Leads إلى قاعدة البيانات.
        """
        if not self.campaign_url:
            return "❌ Campaign API URL is not set."

        response = requests.get(self.campaign_url)
        if response.status_code != 200:
            return f"❌ Failed to fetch data from {self.campaign_url}. Status: {response.status_code}"

        data = response.json()
        new_leads = 0

        # ✅ تأخير استيراد `Lead` إلى وقت التنفيذ فقط
        Lead = apps.get_model("leads", "Lead")

        for lead in data.get("leads", []):
            lead_obj, created = Lead.objects.get_or_create(
                email=lead["email"],
                defaults={
                    "name": lead["name"],
                    "phone": lead.get("phone", None),
                    "campaign": self
                }
            )
            if created:
                new_leads += 1

        self.leads_acquired += new_leads
        self.save()
        return f"✅ Successfully synchronized {new_leads} new leads."

    def generate_report(self):
        """
        ✅ إنشاء تقرير حول أداء الحملة.
        """
        return {
            "Campaign Name": self.name,
            "Platform": self.platform,
            "Status": self.status,
            "Budget": self.budget,
            "Total Spent": self.total_spent,
            "Remaining Budget": self.remaining_budget,
            "Leads Acquired": self.leads_acquired,
            "Revenue Generated": self.revenue_generated,
            "ROI (%)": self.calculate_roi,
        }

    def performance_alert(self):
        """
        ✅ تحديد ما إذا كان يجب إيقاف الحملة أو تعديلها بناءً على الأداء.
        """
        if self.calculate_roi < 10 and self.leads_acquired < 10 and self.total_spent > (self.budget * 0.5):
            return "🚨 Warning: Low ROI and few leads. Consider stopping or adjusting the campaign."
        elif self.calculate_roi > 50 and self.leads_acquired > 20:
            return "✅ Campaign is performing well! Consider increasing the budget."
        else:
            return "ℹ️ Campaign performance is average. Monitor for further adjustments."

    def __str__(self):
        return f"{self.name} ({self.platform}) - {self.status} | ROI: {self.calculate_roi}% | Leads: {self.leads_acquired}"
