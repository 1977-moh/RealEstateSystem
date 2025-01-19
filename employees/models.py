from django.db import models

class Employee(models.Model):
    # خيارات الحقول
    ROLE_CHOICES = [
        ('Sales Manager', 'Sales Manager'),
        ('Marketing Specialist', 'Marketing Specialist'),
        ('Real Estate Agent', 'Real Estate Agent'),
        ('Campaign Manager', 'Campaign Manager'),
        ('Admin', 'Admin'),
    ]

    DEPARTMENT_CHOICES = [
        ('Sales', 'Sales'),
        ('Marketing', 'Marketing'),
        ('Administration', 'Administration'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    # الحقول
    full_name = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, verbose_name="Role")
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, verbose_name="Department")
    hire_date = models.DateField(verbose_name="Hire Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Employee"  # اسم مفرد للنموذج
        verbose_name_plural = "Employees"  # اسم جمع للنموذج
        ordering = ['-hire_date']  # ترتيب السجلات حسب تاريخ التوظيف الأحدث
        constraints = [
            models.UniqueConstraint(fields=['email', 'phone'], name='unique_employee_email_phone')
        ]  # قيود فريدة على البريد الإلكتروني والهاتف

    def __str__(self):
        return f"{self.full_name} - {self.role} ({self.department})"  # عرض الاسم مع الدور والقسم
