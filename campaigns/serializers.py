from rest_framework import serializers
from .models import Campaign
from datetime import date


class CampaignSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لتحويل بيانات الحملة الإعلانية إلى JSON والعكس.
    """

    days_remaining = serializers.SerializerMethodField()  # ✅ حساب الأيام المتبقية للحملة
    daily_budget = serializers.SerializerMethodField()  # ✅ حساب الميزانية اليومية للحملة
    campaign_performance_report = serializers.SerializerMethodField()  # ✅ تقرير أداء الحملة
    currency = serializers.ChoiceField(choices=[("EGP", "EGP"), ("USD", "USD")], default="EGP")  # ✅ دعم العملات

    MAX_BUDGET_USD = 500_000.00  # ✅ الحد الأقصى للميزانية بالدولار
    MAX_BUDGET_EGP = 15_000_000.00  # ✅ الحد الأقصى للميزانية بالجنيه المصري

    class Meta:
        model = Campaign
        fields = '__all__'  # ✅ تضمين جميع الحقول
        read_only_fields = ('created_at', 'updated_at')  # ✅ الحقول الزمنية للقراءة فقط
        extra_kwargs = {
            'name': {'help_text': "📝 أدخل اسم الحملة الإعلانية."},
            'platform': {'help_text': "📢 حدد المنصة المستخدمة للإعلان."},
            'budget': {'help_text': "💰 حدد ميزانية الحملة (يجب أن تكون قيمة موجبة)."},
            'start_date': {'help_text': "📅 حدد تاريخ بدء الحملة."},
            'end_date': {'help_text': "📅 حدد تاريخ انتهاء الحملة."},
            'status': {'help_text': "🟢 حدد حالة الحملة (نشطة، متوقفة، منتهية)."},
            'campaign_url': {'help_text': "🔗 رابط الحملة الإعلانية (اختياري)."},
        }

    def validate(self, data):
        """
        ✅ التحقق من صحة التواريخ بحيث يكون تاريخ الانتهاء بعد تاريخ البداية،
        ✅ ومنع إنشاء حملة بتاريخ بداية في الماضي.
        """
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and start_date < date.today():
            raise serializers.ValidationError({
                "start_date": "📅 لا يمكن بدء الحملة بتاريخ في الماضي!"
            })

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError({
                "end_date": "📅 تاريخ الانتهاء يجب أن يكون لاحقًا لتاريخ البداية!"
            })

        # ✅ التأكد من عدم وجود حملة متداخلة بنفس الاسم والمنصة في نفس الفترة
        if "name" in data and "platform" in data:
            overlapping_campaigns = Campaign.objects.filter(
                name=data["name"],
                platform=data["platform"],
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exclude(id=self.instance.id if self.instance else None)

            if overlapping_campaigns.exists():
                raise serializers.ValidationError({
                    "name": "⚠️ حملة أخرى بنفس الاسم والمنصة موجودة خلال هذه الفترة!"
                })

        return data

    def validate_budget(self, value):
        """
        ✅ التحقق من أن الميزانية موجبة وأقل من الحد الأقصى المحدد بناءً على العملة.
        """
        if value <= 0:
            raise serializers.ValidationError("💰 الميزانية يجب أن تكون رقمًا موجبًا.")

        currency = self.initial_data.get("currency", "EGP")
        max_budget = self.MAX_BUDGET_EGP if currency == "EGP" else self.MAX_BUDGET_USD

        if value > max_budget:
            raise serializers.ValidationError(f"🚨 الحد الأقصى المسموح به للميزانية ({currency}) هو {max_budget:,.2f}.")
        return value

    def get_days_remaining(self, obj):
        """
        ✅ إرجاع عدد الأيام المتبقية حتى انتهاء الحملة، أو `"Expired"` في حال انتهائها.
        """
        remaining_days = (obj.end_date - date.today()).days
        return remaining_days if remaining_days > 0 else "📌 Expired"

    def get_daily_budget(self, obj):
        """
        ✅ إرجاع الميزانية اليومية بناءً على عدد أيام الحملة مع التحقق من أن القسمة لا تتم على صفر.
        """
        total_days = (obj.end_date - obj.start_date).days
        return round(obj.budget / total_days, 2) if total_days > 0 else "⚠️ غير متاح"

    def get_campaign_performance_report(self, obj):
        """
        ✅ تقديم تقرير عن أداء الحملة لتحديد ما إذا كانت ناجحة أو تحتاج إلى تعديل.
        """
        # 🟢 **مثال لحساب النجاح بناءً على الأداء**
        success_threshold = 0.7  # ✅ نسبة النجاح المطلوبة (مثال: 70%)
        leads_generated = obj.leads_acquired  # ✅ عدد العملاء المحتملين الناتجين عن الحملة
        target_leads = 100  # ✅ عدد العملاء المتوقع الحصول عليهم لكل حملة

        success_ratio = leads_generated / target_leads if target_leads > 0 else 0

        if success_ratio >= success_threshold:
            return "✅ الحملة ناجحة، استمر في نفس الإستراتيجية."
        elif 0.4 <= success_ratio < success_threshold:
            return "⚠️ الحملة متوسطة الأداء، يُفضل تحسين المحتوى أو زيادة الميزانية."
        else:
            return "🚨 الحملة ضعيفة، يجب إعادة النظر في استراتيجيتها."

    def sync_active_campaigns(self):
        """
        ✅ مزامنة الحملات النشطة، وتحليل نتائجها، وتحويل البيانات إلى نظام `Leads`.
        """
        active_campaigns = Campaign.objects.filter(status="Active")

        for campaign in active_campaigns:
            # 📊 **تحليل الأداء وسحب بيانات العملاء**
            new_leads = campaign.leads_acquired  # ✅ عدد الليدز المسجلين من الحملة
            budget_performance = campaign.budget / (new_leads + 1)  # ✅ توزيع الميزانية على الليدز

            # 📝 **حفظ التقرير الداخلي للحملة**
            campaign.performance_notes = f"🔹 {new_leads} leads generated | 🔹 Budget Efficiency: {budget_performance:.2f}"
            campaign.save()

        return f"✅ تمت مزامنة {active_campaigns.count()} حملة نشطة وتحليل نتائجها."
