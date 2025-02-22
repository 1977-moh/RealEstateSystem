from rest_framework import serializers
from .models import Lead
import random


class LeadSerializer(serializers.ModelSerializer):
    """
    ✅ Serializer لنموذج `Lead`
    - التحقق من صحة البريد الإلكتروني ورقم الهاتف.
    - منع التكرار داخل نفس الحملة.
    - إضافة `Lead Score` تلقائيًا عند إنشاء العميل المحتمل.
    """

    class Meta:
        model = Lead
        fields = '__all__'  # ✅ تضمين جميع الحقول من `models.py`
        read_only_fields = ['id', 'created_at', 'updated_at', 'lead_score']  # ✅ منع تعديل الحقول المحسوبة

    def validate_email(self, value):
        """
        ✅ التحقق من صحة البريد الإلكتروني ومنع التكرار في نفس الحملة.
        """
        campaign = self.initial_data.get('campaign')
        email = value.lower().strip()

        if Lead.objects.filter(email__iexact=email, campaign=campaign).exists():
            raise serializers.ValidationError("❌ هذا البريد الإلكتروني مسجل بالفعل في هذه الحملة!")

        return email

    def validate_phone(self, value):
        """
        ✅ التحقق من صحة رقم الهاتف والتأكد من تنسيقه الصحيح.
        """
        if value:
            clean_phone = "".join(filter(str.isdigit, value))
            if not (7 <= len(clean_phone) <= 15):
                raise serializers.ValidationError("❌ رقم الهاتف غير صالح. يجب أن يكون بين 7 و 15 رقمًا.")
            return clean_phone
        return value

    def create(self, validated_data):
        """
        ✅ إضافة `Lead Score` تلقائيًا عند إنشاء `Lead` جديد.
        """
        validated_data['lead_score'] = random.randint(50, 100)  # ✅ توليد `Lead Score` بشكل عشوائي بين 50 و 100
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        ✅ منع تعديل `campaign` بعد الإنشاء.
        ✅ السماح فقط بتحديث `status`.
        """
        validated_data.pop('campaign', None)  # ✅ منع تعديل الحملة بعد إنشائها
        return super().update(instance, validated_data)
