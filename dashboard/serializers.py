from rest_framework import serializers
from .models import DashboardStats


class DashboardStatsSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات الإحصائيات إلى JSON مع دعم العملات وتحليل النشاط.
    """
    total_sales_formatted = serializers.SerializerMethodField()  # ✅ عرض إجمالي المبيعات بالعملة المختارة
    activity_level = serializers.SerializerMethodField()  # ✅ تحليل مستوى النشاط بناءً على البيانات
    currency = serializers.ChoiceField(choices=[("EGP", "Egyptian Pound"), ("USD", "US Dollar")], default="EGP")

    class Meta:
        model = DashboardStats
        fields = '__all__'  # ✅ تضمين جميع الحقول
        read_only_fields = ('last_updated',)  # ✅ منع تعديل حقل التحديث التلقائي

    def get_total_sales_formatted(self, obj):
        """
        ✅ تحويل إجمالي المبيعات إلى العملة المختارة وعرضها بتنسيق محسّن.
        """
        exchange_rate = 30.0 if obj.currency == "EGP" else 1.0  # ✅ افتراض 1 USD = 30 EGP

        if obj.total_sales is None:
            return f"0.00 {obj.currency}"

        total_sales_converted = obj.total_sales * exchange_rate
        return f"{total_sales_converted:,.2f} {obj.currency}"

    def get_activity_level(self, obj):
        """
        ✅ تحليل النشاط بناءً على عدد العملاء، العقارات، والمبيعات.
        """
        if obj.total_clients > 200 and obj.total_properties > 100 and obj.total_sales > 1000000:
            return "🚀 Extremely Active"
        elif obj.total_clients > 100 and obj.total_properties > 50 and obj.total_sales > 500000:
            return "📈 Highly Active"
        elif obj.total_clients > 50 and obj.total_properties > 20 and obj.total_sales > 100000:
            return "📊 Moderately Active"
        elif obj.total_clients > 20 and obj.total_properties > 10 and obj.total_sales > 50000:
            return "📉 Low Activity"
        else:
            return "🔻 Very Low Activity"
