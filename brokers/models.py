from django.db import models
from employees.models import Employee

class Broker(models.Model):
    name = models.CharField(max_length=255, verbose_name="Broker Name")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number")
    email = models.EmailField(verbose_name="Email")
    responsible_employee = models.ForeignKey(
        Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsible Employee"
    )
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Commission Rate (%)")
    additional_incentives = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Additional Incentives")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.name


class BrokerClient(models.Model):
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, verbose_name="Broker")
    name = models.CharField(max_length=255, verbose_name="Client Name")
    phone = models.CharField(max_length=20, verbose_name="Client Phone")
    email = models.EmailField(verbose_name="Client Email", blank=True, null=True)
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

    def __str__(self):
        return f"{self.name} ({self.broker.name})"


class EmployeePerformance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Employee")
    broker = models.ForeignKey(Broker, on_delete=models.CASCADE, verbose_name="Broker")
    performance_notes = models.TextField(blank=True, null=True, verbose_name="Performance Notes")
    rewards = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Rewards")
    penalties = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Penalties")
    review_date = models.DateField(auto_now_add=True, verbose_name="Review Date")

    def __str__(self):
        return f"Performance for {self.employee.full_name} on {self.broker.name}"
