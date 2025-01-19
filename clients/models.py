from django.db import models
from django.utils.timezone import now

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name="Client Name")
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Location")
    interests = models.TextField(blank=True, null=True, verbose_name="Interests")
    client_request_details = models.TextField(blank=True, null=True, verbose_name="Request Details")
    entry_date = models.DateTimeField(auto_now_add=True, verbose_name="Entry Date")  # ضبط وقت الإدخال تلقائيًا
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")  # وقت الإنشاء
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")  # وقت التحديث

    class Meta:
        verbose_name = "Client"  # اسم مفرد للنموذج
        verbose_name_plural = "Clients"  # اسم جمع للنموذج
        ordering = ['-created_at']  # ترتيب السجلات بشكل افتراضي حسب الأحدث

    def __str__(self):
        return f"{self.name} - {self.email}"  # تحسين عرض البيانات في قائمة السجلات
