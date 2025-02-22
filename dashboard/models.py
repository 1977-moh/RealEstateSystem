from django.db import models
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.apps import apps  # ✅ لحل مشكلة الاستيراد الدائري
from leads.models import Lead
from properties.models import Property
from campaigns.models import Campaign


class DashboardStats(models.Model):
    """
    ✅ نموذج لإدارة إحصائيات لوحة التحكم مع دعم تحديد العملة.
    """

    CURRENCY_CHOICES = [
        ('EGP', 'Egyptian Pound (EGP)'),
        ('USD', 'US Dollar (USD)'),
    ]

    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='EGP',
        verbose_name="Currency"
    )
    total_employees = models.IntegerField(default=0)
    total_salary_paid = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    total_clients = models.PositiveIntegerField(default=0, verbose_name="Total Clients")
    total_properties = models.PositiveIntegerField(default=0, verbose_name="Total Properties")
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, verbose_name="Total Sales")
    total_commissions = models.DecimalField(max_digits=15, decimal_places=2, default=0.0, verbose_name="Total Commissions")
    active_campaigns = models.PositiveIntegerField(default=0, verbose_name="Active Campaigns")
    total_leads = models.PositiveIntegerField(default=0, verbose_name="Total Leads")
    converted_leads = models.PositiveIntegerField(default=0, verbose_name="Converted Leads")
    conversion_rate = models.FloatField(default=0.0, verbose_name="Conversion Rate (%)")
    highest_performing_employee = models.CharField(max_length=255, blank=True, null=True, verbose_name="Top Employee")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Dashboard Stat"
        verbose_name_plural = "Dashboard Stats"
        ordering = ['-last_updated']

    def __str__(self):
        return f"📊 Dashboard Stats ({self.currency}) - Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("dashboard:stats-detail", kwargs={"pk": self.pk})

    def calculate_conversion_rate(self):
        """✅ حساب معدل تحويل العملاء المحتملين (Leads)."""
        return (self.converted_leads / self.total_leads * 100) if self.total_leads > 0 else 0.0

    def update_stats(self, exchange_rate=30.0):
        """
        ✅ تحديث جميع الإحصائيات بشكل ديناميكي، مع احتساب العمولات داخل الرواتب.
        """
        from clients.models import Client

        # ✅ جلب النماذج عند الحاجة لحل مشكلة الاستيراد الدائري
        Salary = apps.get_model("employees", "Salary")
        EmployeePerformance = apps.get_model("employees", "EmployeePerformance")

        # تحديث إجمالي الموظفين
        self.total_employees = Salary.objects.count()

        # تحديث إجمالي العملاء
        self.total_clients = Client.objects.count()

        # تحديث إجمالي العقارات
        self.total_properties = Property.objects.count()

        # تحديث إجمالي الرواتب
        total_salaries = Salary.objects.aggregate(total=Sum('base_salary'))['total'] or 0.0

        # تحديث إجمالي العمولات من خلال `commission_rate`
        total_commissions = Salary.objects.aggregate(
            total=Sum(ExpressionWrapper(F('base_salary') * (F('commission_rate') / 100), output_field=DecimalField()))
        )['total'] or 0.0

        # تحويل القيم إلى العملة المختارة
        if self.currency == "EGP":
            self.total_sales = total_salaries * exchange_rate
            self.total_commissions = total_commissions * exchange_rate
        else:
            self.total_sales = total_salaries
            self.total_commissions = total_commissions

        # تحديث إجمالي الحملات الإعلانية النشطة
        self.active_campaigns = Campaign.objects.filter(status="Active").count()

        # تحديث إجمالي العملاء المحتملين
        self.total_leads = Lead.objects.count()
        self.converted_leads = Lead.objects.filter(status="Converted").count()

        # حساب معدل التحويل
        self.conversion_rate = self.calculate_conversion_rate()

        # تحديد أفضل موظف بناءً على معدل التحويل
        top_employee = EmployeePerformance.objects.order_by('-conversion_rate').first()
        self.highest_performing_employee = top_employee.employee.full_name if top_employee and top_employee.employee else "No Data"

        # حفظ التحديثات
        self.save()

    @staticmethod
    def update_all_stats(exchange_rate=30.0):
        """✅ تحديث جميع إحصائيات لوحة التحكم دفعة واحدة لجميع السجلات."""
        for stat in DashboardStats.objects.all():
            stat.update_stats(exchange_rate)
