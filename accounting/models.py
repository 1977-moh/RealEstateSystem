from django.db import models
from django.utils.timezone import now
from employees.models import Employee  # ✅ استيراد `Employee` بشكل صحيح


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


class Salary(models.Model):
    """✅ نموذج يمثل رواتب الموظفين مع احتساب العمولة."""
    employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE, related_name="salary_record", verbose_name="Employee"
    )
    base_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Salary")
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Commission Rate (%)")
    commission_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Fixed Commission per Million")
    tax_deduction = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name="Tax Deduction (%)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Salary"
        verbose_name_plural = "Salaries"

    def __str__(self):
        return f"{self.employee.full_name} - Base: ${self.base_salary} - Tax: {self.tax_deduction}%"

    @property
    def computed_salary(self):
        """✅ حساب الراتب الصافي بعد الضرائب."""
        tax_amount = (self.tax_deduction / 100) * self.base_salary
        return self.base_salary - tax_amount


class SalesCommission(models.Model):
    """✅ نموذج لحساب العمولات بناءً على مبيعات الموظف."""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee_commissions", verbose_name="Employee"
    )
    sales_amount = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Total Sales")
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Commission Earned", blank=True, null=True)
    date_calculated = models.DateField(default=now, verbose_name="Commission Date")

    class Meta:
        ordering = ['-date_calculated']
        verbose_name = "Sales Commission"
        verbose_name_plural = "Sales Commissions"

    def __str__(self):
        return f"{self.employee.full_name} - Sales: ${self.sales_amount} - Commission: ${self.commission_earned}"

    def save(self, *args, **kwargs):
        """✅ حساب العمولة تلقائيًا عند الحفظ."""
        salary = Salary.objects.filter(employee=self.employee).first()
        self.commission_earned = self.sales_amount * (salary.commission_rate / 100) if salary else 0.00
        super().save(*args, **kwargs)


class IncentiveType(models.Model):
    """✅ نموذج يمثل أنواع الحوافز المالية للموظفين."""
    name = models.CharField(max_length=255, unique=True, verbose_name="Incentive Type Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Incentive Type"
        verbose_name_plural = "Incentive Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class DeductionType(models.Model):
    """✅ نموذج يمثل أنواع الخصومات المالية للموظفين."""
    name = models.CharField(max_length=255, unique=True, verbose_name="Deduction Type Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name = "Deduction Type"
        verbose_name_plural = "Deduction Types"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Bonus(models.Model):
    """✅ نموذج يمثل المكافآت المالية التي يحصل عليها الموظفون."""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee_bonuses", verbose_name="Employee"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Bonus Amount")
    reason = models.TextField(blank=True, null=True, verbose_name="Reason for Bonus")
    date_given = models.DateField(auto_now_add=True, verbose_name="Date Given")

    class Meta:
        verbose_name = "Bonus"
        verbose_name_plural = "Bonuses"
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.employee.full_name} - Bonus: {self.amount} on {self.date_given}"


class Deduction(models.Model):
    """✅ نموذج يمثل الخصومات المالية التي يتم اقتطاعها من الموظفين."""
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="employee_deductions", verbose_name="Employee"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Deduction Amount")
    reason = models.TextField(blank=True, null=True, verbose_name="Reason for Deduction")
    date_given = models.DateField(auto_now_add=True, verbose_name="Date Given")

    class Meta:
        verbose_name = "Deduction"
        verbose_name_plural = "Deductions"
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.employee.full_name} - Deduction: {self.amount} on {self.date_given}"
