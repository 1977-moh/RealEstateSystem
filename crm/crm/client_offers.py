from .models import AIRecommendation, ClientActivity
from .notifications import NotificationManager
from django.utils.timezone import now
import random

# ✅ تهيئة مدير الإشعارات
notifier = NotificationManager()


def send_client_offers():
    """
    ✅ إرسال العروض بناءً على تحليل الذكاء الصناعي.
    """
    recommendations = AIRecommendation.objects.filter(confidence_score__gte=0.7)

    for rec in recommendations:
        client = rec.client
        message = f"👋 مرحبًا {client.name}، لدينا عرض خاص لك: {rec.recommended_offer} 🎯"
        sent_methods = []

        # ✅ إرسال البريد الإلكتروني
        if client.email:
            email_sent = notifier.send_email(client.email, "🎯 عرض خاص لك!", message)
            if email_sent:
                sent_methods.append("Email")

        # ✅ إرسال عبر واتساب
        if client.phone:
            whatsapp_sent = notifier.send_whatsapp(client.phone, message)
            if whatsapp_sent:
                sent_methods.append("WhatsApp")

        # ✅ إرسال SMS
        if client.phone:
            sms_sent = notifier.send_sms(client.phone, message)
            if sms_sent:
                sent_methods.append("SMS")

        # ✅ إرسال إشعار Push عبر Firebase
        if client.fcm_token:
            push_sent = notifier.send_push_notification("🎉 عرض حصري!", message, client.fcm_token)
            if push_sent:
                sent_methods.append("Push Notification")

        # ✅ إرسال إشعار Telegram إذا كان العميل متابعًا
        telegram_sent = notifier.send_telegram_message(f"📣 {message}")
        if telegram_sent:
            sent_methods.append("Telegram")

        # ✅ تسجيل العرض المرسل في `ClientActivity`
        ClientActivity.objects.create(
            client=client,
            activity_type="offer_sent",
            notes=f"📩 العرض أرسل عبر: {', '.join(sent_methods)}",
            timestamp=now()
        )

        print(f"✅ تم إرسال العرض إلى {client.name} عبر: {', '.join(sent_methods)}")


# 🌟 تشغيله يدويًا أو عبر Celery في `tasks.py`
if __name__ == "__main__":
    send_client_offers()
