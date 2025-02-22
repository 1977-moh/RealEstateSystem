import os
import logging
from celery import Celery

# ✅ ضبط إعدادات البيئة لـ Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'real_estate_system.settings')

# ✅ إنشاء كائن Celery وتحميل الإعدادات من Django
app = Celery('real_estate_system')
app.config_from_object('django.conf:settings', namespace='CELERY')

# ✅ البحث تلقائيًا عن جميع المهام داخل التطبيقات المسجلة في Django
app.autodiscover_tasks()

# === ⚡ تحسين تسجيل الأحداث (Logging) ===
logger = logging.getLogger(__name__)

@app.task(bind=True)
def debug_task(self):
    """
    ✅ اختبار تشغيل Celery
    """
    logger.info(f"✅ Celery is running successfully! Task ID: {self.request.id}")
    return f"✅ Celery Task Executed: {self.request.id}"

# === 🔄 تحسين التعامل مع المهام الفاشلة ===
@app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def robust_task(self):
    """
    ✅ مثال لمهمة تحاول إعادة التشغيل تلقائيًا عند الفشل.
    """
    try:
        # 🔹 رمز المهمة التجريبية هنا (مثال: استيراد بيانات العملاء المحتملين)
        logger.info(f"🚀 Running Robust Task: {self.request.id}")
        # ❌ محاكاة خطأ لغرض الاختبار
        raise ValueError("❌ Simulated Failure!")
    except Exception as e:
        logger.error(f"⚠️ Task Failed! Error: {e}")
        raise self.retry(exc=e)

# === ⏳ تمكين دعم Celery Beat ===
@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    ✅ ضبط المهام المجدولة باستخدام Celery Beat
    """
    from celery.schedules import crontab

    sender.add_periodic_task(
        crontab(hour=0, minute=0),  # ✅ تشغيل المهمة يوميًا في منتصف الليل
        debug_task.s(),
        name="🔄 تشغيل اختبار Celery يوميًا"
    )

    sender.add_periodic_task(
        crontab(hour='*/6', minute=0),  # ✅ تشغيل كل 6 ساعات
        robust_task.s(),
        name="🔄 تشغيل المهام الذكية كل 6 ساعات"
    )

# === ✅ تشغيل Celery مع Beat ===
if __name__ == "__main__":
    app.start()
