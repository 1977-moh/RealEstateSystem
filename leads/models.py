from django.db import models
from campaigns.models import Campaign
from employees.models import Employee


class Lead(models.Model):
    """
    نموذج لتمثيل العملاء المتوقعين في النظام.
    """
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        verbose_name="Related Campaign"
    )
    name = models.CharField(max_length=255, verbose_name="Lead Name")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Phone")
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Assigned Employee"
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("New", "New"),
            ("In Progress", "In Progress"),
            ("Closed", "Closed"),
        ],
        default="New",
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']  # ترتيب العملاء حسب الأحدث
        verbose_name = "Lead"
        verbose_name_plural = "Leads"

    def __str__(self):
        return self.name
