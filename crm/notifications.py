import smtplib
import requests
import json
import logging
from twilio.rest import Client as TwilioClient
from firebase_admin import messaging, credentials, initialize_app
from django.conf import settings
from django.utils.timezone import now
from celery import shared_task
from .models import Client, AIRecommendation

# ✅ إعداد تسجيل الأخطاء
logger = logging.getLogger(__name__)

# ✅ تحميل بيانات Firebase Cloud Messaging
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_app = initialize_app(cred)


class NotificationManager:
    """
    ✅ مدير الإشعارات الذكي باستخدام AI & Celery
    """
    def __init__(self):
        self.twilio_client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.sender_email = settings.EMAIL_HOST_USER
        self.smtp_server = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.smtp_password = settings.EMAIL_HOST_PASSWORD
        self.telegram_token = settings.TELEGRAM_BOT_TOKEN
        self.telegram_chat_id = settings.TELEGRAM_CHAT_ID

    def send_email(self, recipient, subject, message):
        """
        ✅ إرسال بريد إلكتروني + تحليل تجاوب العميل
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.smtp_password)
                email_message = f"Subject: {subject}\n\n{message}"
                server.sendmail(self.sender_email, recipient, email_message)

            self.update_client_engagement(recipient, "email")
            logger.info(f"📩 تم إرسال البريد إلى {recipient}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إرسال البريد: {e}")
            return False

    def send_whatsapp(self, recipient_phone, message):
        """
        ✅ إرسال رسالة واتساب + تحليل تجاوب العميل
        """
        try:
            self.twilio_client.messages.create(
                body=message,
                from_="whatsapp:+14155238886",
                to=f"whatsapp:{recipient_phone}"
            )

            self.update_client_engagement(recipient_phone, "whatsapp")
            logger.info(f"📲 تم إرسال واتساب إلى {recipient_phone}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إرسال واتساب: {e}")
            return False

    def send_sms(self, recipient_phone, message):
        """
        ✅ إرسال رسالة SMS + تحليل تجاوب العميل
        """
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=recipient_phone
            )

            self.update_client_engagement(recipient_phone, "sms")
            logger.info(f"📩 تم إرسال SMS إلى {recipient_phone}")
            return True
        except Exception as e:
            logger.error(f"❌ فشل إرسال SMS: {e}")
            return False

    def send_push_notification(self, title, message, client_fcm_token):
        """
        ✅ إرسال إشعارات Push عبر Firebase + تحليل تجاوب العميل
        """
        try:
            notification_message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=client_fcm_token,
            )
            response = messaging.send(notification_message)

            self.update_client_engagement(client_fcm_token, "push")
            logger.info(f"🔔 تم إرسال إشعار Push إلى {client_fcm_token}")
            return response
        except Exception as e:
            logger.error(f"❌ فشل إرسال Push Notification: {e}")
            return None

    def send_telegram_message(self, message):
        """
        ✅ إرسال رسالة عبر Telegram Bot
        """
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                "chat_id": self.telegram_chat_id,
                "text": message
            }
            response = requests.post(url, json=data)

            if response.status_code == 200:
                logger.info("✅ تم إرسال إشعار Telegram")
                return True
            else:
                logger.error(f"❌ فشل إرسال Telegram: {response.text}")
                return False
        except Exception as e:
            logger.error(f"❌ خطأ في إرسال Telegram: {e}")
            return False

    def update_client_engagement(self, identifier, method):
        """
        ✅ تحديث بيانات العميل في CRM بناءً على طريقة الاتصال
        """
        try:
            if "@" in identifier:
                client = Client.objects.filter(email=identifier).first()
            else:
                client = Client.objects.filter(phone=identifier).first()

            if client:
                AIRecommendation.objects.create(
                    client=client,
                    recommended_offer="🎯 عرض جديد بناءً على سلوكك!",
                    confidence_score=0.9
                )
                logger.info(f"🔄 تحديث سلوك العميل: {client.name} ({method})")
        except Exception as e:
            logger.error(f"❌ فشل تحديث سلوك العميل: {e}")

    @shared_task
    def schedule_notifications():
        """
        ✅ جدولة الإشعارات تلقائيًا عبر Celery
        """
        clients = Client.objects.filter(status="potential")

        for client in clients:
            message = f"👋 مرحبًا {client.name}! هل ترغب في معرفة أحدث العروض؟"
            subject = "🔥 عروض عقارية جديدة لك!"

            if client.status == "vip":
                NotificationManager().send_email(client.email, subject, message)
                NotificationManager().send_whatsapp(client.phone, message)
                NotificationManager().send_push_notification(subject, message, client.fcm_token)
                NotificationManager().send_telegram_message(f"💎 إشعار VIP: {message}")

            elif client.status == "active":
                NotificationManager().send_email(client.email, subject, message)
                NotificationManager().send_whatsapp(client.phone, message)

            elif client.status == "potential":
                NotificationManager().send_whatsapp(client.phone, message)

            else:
                NotificationManager().send_email(client.email, subject, message)

        logger.info(f"🔔 تم جدولة الإشعارات لـ {clients.count()} عملاء محتملين")


# ✅ **مثال استخدام**
if __name__ == "__main__":
    notifier = NotificationManager()
    notifier.send_email("client@example.com", "🎯 عرض خاص لك!", "🔥 خصم 30% على العقارات الفاخرة!")
    notifier.send_whatsapp("+201234567890", "🎉 لديك عرض جديد!")
    notifier.send_sms("+201234567890", "💰 تحقق من أحدث عروض العقارات!")
    notifier.send_telegram_message("📣 إشعار خاص بعملاء العقارات!")
