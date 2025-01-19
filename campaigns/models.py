from django.db import models


class Campaign(models.Model):
    PLATFORM_CHOICES = [
        ("Facebook", "Facebook"),
        ("Google", "Google Ads"),
        ("TikTok", "TikTok Ads"),
        ("Instagram", "Instagram"),
        ("LinkedIn", "LinkedIn"),
    ]
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Paused", "Paused"),
        ("Completed", "Completed"),
    ]

    name = models.CharField(max_length=255, verbose_name="Campaign Name")
    platform = models.CharField(
        max_length=50,
        choices=PLATFORM_CHOICES,
        verbose_name="Advertising Platform"
    )
    budget = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Budget")
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Status"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    campaign_url = models.URLField(blank=True, null=True, verbose_name="Campaign URL")  # رابط الحملة

    # إضافة قيود لمنع التكرار في الاسم والمنصة
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'platform'], name='unique_campaign_per_platform')
        ]
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return f"{self.name} ({self.platform})"
