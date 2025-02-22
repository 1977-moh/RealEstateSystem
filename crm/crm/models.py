import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import EmailValidator, MinValueValidator, MaxValueValidator
from employees.models import Employee
from campaigns.models import Campaign


class Client(models.Model):
    """
    ✅ نموذج العميل الأساسي مع تحسينات وسائل التواصل الاجتماعي والتحليل الذكي.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Client Name")
    email = models.EmailField(unique=True, validators=[EmailValidator()], verbose_name="Email Address")
    phone = models.CharField(max_length=20, verbose_name="Phone Number", unique=True)
    address = models.TextField(blank=True, verbose_name="Address")

    # 🔥 الموقع الجغرافي لتقديم العروض بناءً على الموقع
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")

    CLIENT_SOURCES = [
        ('advertisement', 'Advertisement'),
        ('referral', 'Referral'),
        ('website', 'Website Inquiry'),
        ('social_media', 'Social Media'),
        ('direct_contact', 'Direct Contact'),
        ('ai_detected', 'AI-Detected'),
        ('other', 'Other'),
    ]
    client_source = models.CharField(max_length=50, choices=CLIENT_SOURCES, default='other')

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('potential', 'Potential'),
        ('vip', 'VIP'),
        ('follow_up', 'Follow-Up Needed'),
        ('recurrent_buyer', 'Recurrent Buyer'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='potential')

    # 🔥 حسابات وسائل التواصل الاجتماعي
    facebook = models.URLField(blank=True, null=True, verbose_name="Facebook Profile")
    twitter = models.URLField(blank=True, null=True, verbose_name="Twitter Profile")
    linkedin = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")
    google = models.URLField(blank=True, null=True, verbose_name="Google Profile")
    tiktok = models.URLField(blank=True, null=True, verbose_name="TikTok Profile")
    instagram = models.URLField(blank=True, null=True, verbose_name="Instagram Profile")

    # 🔥 مستوى تفاعل العميل عبر وسائل التواصل الاجتماعي
    social_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
                                     verbose_name="Social Engagement Score")

    # 🔥 آخر تحديث لبيانات التواصل الاجتماعي
    last_social_update = models.DateTimeField(null=True, blank=True, verbose_name="Last Social Update")

    assigned_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name="clients")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def update_interest_level(self):
        """
        ✅ تحليل مستوى الاهتمام بناءً على الأنشطة السابقة.
        """
        activities = self.activities.count()
        if activities > 5:
            self.status = 'follow_up'
        if activities > 10:
            self.status = 'vip'
        self.save()


class Lead(models.Model):
    """
    ✅ نموذج تسجيل العملاء المحتملين مع تحليل الذكاء الصناعي لتحديد الأولوية.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="leads")
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE, related_name="crm_leads")  # ✅ حل التعارض
    interest_level = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(10)],
                                         help_text="Interest level from 1 to 10")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lead: {self.client.name} (Campaign: {self.campaign})"


class ClientActivity(models.Model):
    """
    ✅ سجل الأنشطة والتفاعلات مع العميل، بما في ذلك الزيارات والاجتماعات.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=100, choices=[
        ('call', 'Call'),
        ('meeting', 'Meeting'),
        ('email', 'Email'),
        ('offer_sent', 'Offer Sent'),
        ('purchase', 'Purchase'),
        ('follow_up', 'Follow-Up'),
        ('visit', 'Site Visit'),
    ])
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.client.name} - {self.activity_type} ({self.timestamp})"


class AIRecommendation(models.Model):
    """
    ✅ تحليل الذكاء الاصطناعي لاقتراح العروض المناسبة للعملاء بناءً على التفاعل.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="recommendations")
    recommended_offer = models.TextField()
    confidence_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Recommendation for {self.client.name} - Confidence: {self.confidence_score:.2f}"


class ClientVisit(models.Model):
    """
    ✅ سجل الزيارات التي يقوم بها العميل لمواقع العقارات.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="visits")
    property_id = models.CharField(max_length=100, verbose_name="Property ID")
    visit_date = models.DateTimeField(default=now)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Visit - {self.client.name} to Property {self.property_id} on {self.visit_date}"
