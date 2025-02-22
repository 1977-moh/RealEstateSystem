from rest_framework import serializers
from .models import Client, Lead, ClientActivity, AIRecommendation


class ClientSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لإدارة بيانات العملاء مع تحليل ذكي.
    """
    days_since_registration = serializers.SerializerMethodField()
    client_status_display = serializers.SerializerMethodField()
    social_score = serializers.FloatField(read_only=True)

    class Meta:
        model = Client
        fields = '__all__'

    def get_days_since_registration(self, obj):
        """
        ✅ إرجاع عدد الأيام منذ تسجيل العميل.
        """
        return (obj.created_at.date() - obj.created_at.date()).days

    def get_client_status_display(self, obj):
        """
        ✅ إرجاع النص الكامل لحالة العميل.
        """
        return obj.get_status_display()


class LeadSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحليل العملاء المحتملين وتقدير أولوياتهم.
    """
    client_name = serializers.CharField(source='client.name', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    interest_level_display = serializers.SerializerMethodField()

    class Meta:
        model = Lead
        fields = '__all__'

    def get_interest_level_display(self, obj):
        """
        ✅ تصنيف العميل بناءً على مستوى الاهتمام (1-10).
        """
        if obj.interest_level >= 8:
            return "High Interest"
        elif obj.interest_level >= 5:
            return "Medium Interest"
        return "Low Interest"


class ClientActivitySerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحليل التفاعل مع العملاء.
    """
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = ClientActivity
        fields = '__all__'


class AIRecommendationSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لاقتراح العروض بناءً على الذكاء الصناعي.
    """
    confidence_level = serializers.SerializerMethodField()
    client_name = serializers.CharField(source='client.name', read_only=True)

    class Meta:
        model = AIRecommendation
        fields = '__all__'

    def get_confidence_level(self, obj):
        """
        ✅ تحويل الثقة إلى مستوى سهل القراءة.
        """
        if obj.confidence_score >= 0.8:
            return "Highly Recommended"
        elif obj.confidence_score >= 0.5:
            return "Moderate Recommendation"
        return "Low Confidence"
