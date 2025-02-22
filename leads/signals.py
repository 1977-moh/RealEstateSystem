from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import model_to_dict
from .models import Lead

# ✅ استيراد `send_email` و `send_whatsapp_message` بطريقة آمنة
try:
    from notifications.helpers import send_email, send_whatsapp_message
    from notifications.utils import id2slug
    from notifications.settings import get_config
except ImportError:
    print("⚠️ لم يتم العثور على `send_email` أو `send_whatsapp_message` في `notifications.helpers`، تأكد من وجودها!")


def get_num_to_fetch(request):
    """
    ✅ استرداد عدد الإشعارات المطلوب جلبها، مع التأكد من القيم الصحيحة.
    """
    default_num_to_fetch = get_config().get('NUM_TO_FETCH', 5)  # افتراضي: 5 إشعارات
    try:
        num_to_fetch = int(request.GET.get('max', default_num_to_fetch))
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:
        num_to_fetch = default_num_to_fetch
    return num_to_fetch


def get_notification_list(request, method_name='all'):
    """
    ✅ إرجاع قائمة الإشعارات بصيغة JSON جاهزة للاستعمال.
    """
    num_to_fetch = get_num_to_fetch(request)
    notification_list = []

    for notification in getattr(request.user.notifications, method_name)()[0:num_to_fetch]:
        struct = model_to_dict(notification)
        struct['slug'] = id2slug(notification.id)

        if notification.actor:
            struct['actor'] = str(notification.actor)
        if notification.target:
            struct['target'] = str(notification.target)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)
        if notification.data:
            struct['data'] = notification.data

        notification_list.append(struct)

        if request.GET.get('mark_as_read'):
            notification.mark_as_read()

    return notification_list


@receiver(post_save, sender=Lead)
def send_lead_followup(sender, instance, created, **kwargs):
    """
    ✅ عند إنشاء `Lead` جديد، يتم إرسال رسالة متابعة تلقائيًا عبر البريد وواتساب.
    """
    if created:
        message = f"""
        👋 مرحبًا {instance.name}، شكرًا على اهتمامك بعروضنا العقارية! 🏡
        سنكون سعداء بمساعدتك في العثور على العقار المثالي. 
        لا تتردد في التواصل معنا لأي استفسار. 📞
        """

        # 📩 إرسال بريد إلكتروني
        try:
            send_email(instance.email, "🎯 شكرًا لاهتمامك! - متابعتك من فريقنا", message)
        except Exception as e:
            print(f"⚠️ فشل إرسال البريد الإلكتروني إلى {instance.email}: {e}")

        # 📲 إرسال رسالة واتساب
        if instance.phone:
            try:
                send_whatsapp_message(instance.phone, message)
            except Exception as e:
                print(f"⚠️ فشل إرسال رسالة واتساب إلى {instance.phone}: {e}")

        print(f"✅ تم إرسال المتابعة إلى {instance.email} و {instance.phone if instance.phone else '🚫 بدون واتساب'}")
