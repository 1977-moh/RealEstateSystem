import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date
from django.db.models import Count
from django.apps import apps  # ✅ لحل مشكلة الاستيراد الدائري


class Department(models.Model):
    """✅ نموذج يمثل أقسام الشركة."""
    name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    """✅ نموذج يمثل المسميات الوظيفية داخل الشركة."""
    title = models.CharField(max_length=255, unique=True, verbose_name="Job Title")
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="job_titles", verbose_name="Department"
    )

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.department.name})"


class Employee(models.Model):
    """✅ نموذج يمثل بيانات الموظفين داخل الشركة العقارية."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('On Leave', 'On Leave'),
        ('Retired', 'Retired'),
    ]

    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Phone Number")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    address = models.TextField(null=True, blank=True, verbose_name="Address")

    job_title = models.ForeignKey(JobTitle, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Job Title")
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="employees", verbose_name="Department"
    )

    hire_date = models.DateField(default=now, verbose_name="Hire Date")
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Salary")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name="Status")

    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        ordering = ['-hire_date']
        constraints = [
            models.UniqueConstraint(fields=['email', 'phone'], name='unique_employee_email_phone')
        ]

    def __str__(self):
        return f"{self.full_name} - {self.job_title} ({self.department}) [{self.status}]"

    def clean(self):
        """✅ التحقق من صحة البيانات قبل الحفظ."""
        if not self.email.endswith("@company.com"):
            raise ValidationError("❌ البريد الإلكتروني يجب أن ينتهي بـ '@company.com'.")
        if self.hire_date > now().date():
            raise ValidationError("❌ لا يمكن أن يكون تاريخ التوظيف في المستقبل.")
        if self.birth_date and self.birth_date > now().date():
            raise ValidationError("❌ لا يمكن أن يكون تاريخ الميلاد في المستقبل.")
        if self.salary < 0:
            raise ValidationError("❌ الراتب لا يمكن أن يكون رقمًا سالبًا.")


class EmployeePerformance(models.Model):
    """✅ نموذج تقييم الأداء استنادًا إلى تحويل العملاء المتوقعين."""
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name="performance", verbose_name="Employee"
    )

    total_leads = models.PositiveIntegerField(default=0, verbose_name="Total Leads")
    converted_leads = models.PositiveIntegerField(default=0, verbose_name="Converted Leads")
    conversion_rate = models.FloatField(default=0.0, verbose_name="Conversion Rate (%)")
    last_review_date = models.DateField(default=now, verbose_name="Last Review Date")

    class Meta:
        verbose_name = "Employee Performance"
        verbose_name_plural = "Employee Performance Reports"

    def update_performance(self):
        """✅ تحديث الأداء باستخدام `apps.get_model()` لحل مشكلة الاستيراد الدائري."""
        Lead = apps.get_model("leads", "Lead")  # ✅ جلب النموذج عند الحاجة

        stats = Lead.objects.filter(assigned_to=self.employee).aggregate(
            total_leads=Count('id'),
            converted_leads=Count('id', filter=models.Q(status="Converted"))
        )

        self.total_leads = stats.get("total_leads", 0) or 0
        self.converted_leads = stats.get("converted_leads", 0) or 0
        self.conversion_rate = (self.converted_leads / self.total_leads * 100) if self.total_leads > 0 else 0
        self.last_review_date = date.today()
        self.save()

    def __str__(self):
        return f"{self.employee.full_name} - {self.conversion_rate:.2f}% Conversion"


class SalesCommission(models.Model):
    """✅ نموذج لحساب العمولات بناءً على مبيعات الموظف."""
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="commissions",  # ✅ تم تعديل `related_name` لحل التعارض
        verbose_name="Employee"
    )

    sales_amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Total Sales"
    )

    commission_earned = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Commission Earned",
        blank=True,
        null=True
    )

    date_calculated = models.DateField(
        auto_now_add=True,
        verbose_name="Commission Date"
    )

    class Meta:
        ordering = ['-date_calculated']
        verbose_name = "Sales Commission"
        verbose_name_plural = "Sales Commissions"

    def save(self, *args, **kwargs):
        """✅ حل مشكلة استيراد `Salary` ديناميكيًا عند الحفظ."""
        Salary = apps.get_model("employees", "Salary")  # ✅ جلب النموذج ديناميكيًا
        salary = Salary.objects.filter(employee=self.employee).first()

        if salary:
            self.commission_earned = self.sales_amount * (salary.commission_rate / 100)
        else:
            self.commission_earned = 0.0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name} - Sales: ${self.sales_amount} - Commission: ${self.commission_earned}"
