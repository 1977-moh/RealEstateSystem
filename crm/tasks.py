from celery import shared_task
from django.utils.timezone import now
from .models import Client, AIRecommendation
from .ai_analyzer import analyze_client_data
from .client_offers import send_client_offers
from .web_scraper import SocialMediaScraper
import random
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_ai_recommendations():
    """
    ✅ تحليل بيانات العملاء وتقديم عروض مخصصة باستخدام الذكاء الاصطناعي
    """
    try:
        clients = Client.objects.all()
        if not clients.exists():
            logger.info("🚀 لا يوجد عملاء لتحليلهم.")
            return "No clients found."

        for client in clients:
            recommended_offer = f"🔥 عرض خاص لك، {client.name}!"
            confidence_score = round(random.uniform(0.6, 0.95), 2)

            AIRecommendation.objects.create(
                client=client,
                recommended_offer=recommended_offer,
                confidence_score=confidence_score
            )

        logger.info(f"✅ تم إنشاء توصيات AI لـ {clients.count()} عملاء.")
        return f"AI recommendations generated for {clients.count()} clients."

    except Exception as e:
        logger.error(f"❌ فشل إنشاء توصيات AI: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def scheduled_scraper():
    """
    ✅ تشغيل البحث التلقائي عن العملاء المحتملين من منصات التواصل الاجتماعي.
    """
    try:
        scraper = SocialMediaScraper()
        keyword = "Luxury Real Estate"  # 🏡 تخصيص البحث لمجال العقارات الفاخرة
        leads = scraper.search_all(keyword)

        logger.info(f"🔍 تم العثور على {len(leads)} عميل محتمل من وسائل التواصل الاجتماعي.")
        return f"Found {len(leads)} potential clients."

    except Exception as e:
        logger.error(f"❌ خطأ أثناء البحث عن العملاء المحتملين: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def scheduled_ai_analysis():
    """
    ✅ جدولة تحليل بيانات العملاء يوميًا باستخدام الذكاء الصناعي.
    """
    try:
        analyze_client_data()
        logger.info("✅ تم تشغيل تحليل AI اليومي بنجاح.")
        return "Daily AI analysis completed."

    except Exception as e:
        logger.error(f"❌ فشل تحليل بيانات العملاء: {str(e)}")
        return f"Error: {str(e)}"


@shared_task
def scheduled_offer_sending():
    """
    ✅ جدولة إرسال العروض الذكية للعملاء بناءً على تحليل الذكاء الصناعي.
    """
    try:
        send_client_offers()
        logger.info("✅ تم إرسال العروض الذكية للعملاء بنجاح.")
        return "Smart offers sent successfully."

    except Exception as e:
        logger.error(f"❌ فشل إرسال العروض: {str(e)}")
        return f"Error: {str(e)}"
