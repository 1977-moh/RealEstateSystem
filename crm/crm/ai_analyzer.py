import random
import openai
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from .models import Client, AIRecommendation, ClientActivity
from .web_scraper import SocialMediaScraper
from datetime import datetime, timedelta


class AIAnalyzer:
    """
    ✅ أداة تحليل الذكاء الاصطناعي للعملاء المحتملين وإعطاء توصيات ذكية.
    """

    def __init__(self):
        self.scraper = SocialMediaScraper()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        openai.api_key = "your_openai_api_key"  # 🔑 أدخل مفتاح API

    def analyze_client_engagement(self, client):
        """
        ✅ تحليل تفاعل العميل بناءً على النشاط السابق.
        """
        activities = ClientActivity.objects.filter(client=client)
        engagement_score = len(activities) * 0.1  # 10% لكل نشاط سابق

        if client.status == "vip":
            engagement_score += 0.3  # ✅ إعطاء أهمية أكبر لعملاء VIP
        elif client.status == "inactive":
            engagement_score -= 0.2  # ⚠️ تقليل الأولوية للعملاء غير النشطين

        return round(min(engagement_score, 1.0), 2)

    def analyze_social_media_interest(self, keyword):
        """
        ✅ البحث عن العملاء المحتملين وتحليل اهتماماتهم.
        """
        results = self.scraper.search_all(keyword)
        return len(results) * 0.05  # ✅ تحويل عدد النتائج إلى نسبة اهتمام

    def generate_ai_recommendation(self, client):
        """
        ✅ استخدام ChatGPT لإنشاء توصية مخصصة لكل عميل.
        """
        prompt = f"""
        عميل اسمه {client.name} لديه سجل مشتريات سابق واهتمام بالعقارات الفاخرة.
        كيف يمكننا تقديم عرض يجذب هذا العميل بناءً على البيانات المتاحة؟
        """
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]

    def analyze_all_clients(self):
        """
        ✅ تحليل جميع العملاء وتحديث توصياتهم في النظام.
        """
        for client in Client.objects.all():
            engagement_score = self.analyze_client_engagement(client)
            social_interest = self.analyze_social_media_interest(client.name)

            final_score = self.scaler.fit_transform(
                np.array([[engagement_score + social_interest]])
            )[0][0]

            recommendation = self.generate_ai_recommendation(client)

            AIRecommendation.objects.update_or_create(
                client=client,
                defaults={
                    "recommended_offer": recommendation,
                    "confidence_score": round(final_score, 2),
                    "generated_at": datetime.now()
                }
            )
            print(f"🤖 تحليل {client.name} - ثقة: {round(final_score, 2)}")


# ✅ تشغيل التحليل تلقائيًا عبر Celery كل 24 ساعة
def scheduled_ai_analysis():
    ai_analyzer = AIAnalyzer()
    ai_analyzer.analyze_all_clients()
