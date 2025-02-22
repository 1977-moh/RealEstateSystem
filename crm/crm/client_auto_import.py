import csv
import pandas as pd
import logging
from django.utils.timezone import now
from .models import Client, Lead
from .web_scraper import SocialMediaScraper
from .ai_analyzer import AIAnalyzer

logger = logging.getLogger(__name__)


class ClientAutoImporter:
    """
    ✅ أداة استيراد العملاء المحتملين تلقائيًا من وسائل التواصل الاجتماعي وملفات البيانات.
    """

    def __init__(self):
        self.scraper = SocialMediaScraper()
        self.ai_analyzer = AIAnalyzer()

    def import_from_social_media(self, keyword):
        """
        ✅ البحث عن العملاء المحتملين في وسائل التواصل الاجتماعي واستيرادهم تلقائيًا.
        """
        new_clients = []
        results = self.scraper.search_all(keyword)

        for result in results:
            email = result.get("email", "").strip()
            phone = result.get("phone", "").strip()

            # ✅ التحقق من وجود العميل مسبقًا
            if Client.objects.filter(email=email).exists() or Client.objects.filter(phone=phone).exists():
                logger.info(f"📌 العميل {result['name']} موجود مسبقًا.")
                continue

            # ✅ إنشاء سجل جديد
            client = Client.objects.create(
                name=result["name"],
                email=email,
                phone=phone,
                address=result.get("location", ""),
                client_source="social_media",
                status="potential",
                created_at=now()
            )
            new_clients.append(client)
            logger.info(f"✅ تم استيراد العميل {client.name} من وسائل التواصل الاجتماعي.")

        # 🔄 تشغيل تحليل الذكاء الاصطناعي بعد الاستيراد
        self.ai_analyzer.analyze_all_clients()
        return new_clients

    def import_from_csv(self, file_path):
        """
        ✅ استيراد العملاء المحتملين من ملفات CSV.
        """
        new_clients = []
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    email = row.get("Email", "").strip()
                    phone = row.get("Phone", "").strip()

                    # ✅ التحقق من تكرار العميل
                    if Client.objects.filter(email=email).exists() or Client.objects.filter(phone=phone).exists():
                        logger.info(f"📌 العميل {row['Name']} موجود مسبقًا.")
                        continue

                    # ✅ إنشاء سجل جديد
                    client = Client.objects.create(
                        name=row["Name"],
                        email=email,
                        phone=phone,
                        address=row.get("Address", ""),
                        client_source=row.get("Source", "other"),
                        status=row.get("Status", "potential"),
                        created_at=now()
                    )
                    new_clients.append(client)
                    logger.info(f"✅ تم استيراد العميل {client.name} من CSV.")

            # 🔄 تشغيل تحليل الذكاء الاصطناعي بعد الاستيراد
            self.ai_analyzer.analyze_all_clients()
        except Exception as e:
            logger.error(f"❌ خطأ أثناء استيراد البيانات من CSV: {str(e)}")
        return new_clients

    def import_from_excel(self, file_path):
        """
        ✅ استيراد العملاء من ملفات Excel.
        """
        new_clients = []
        try:
            df = pd.read_excel(file_path)

            for _, row in df.iterrows():
                email = str(row.get("Email", "")).strip()
                phone = str(row.get("Phone", "")).strip()

                # ✅ التحقق من عدم التكرار
                if Client.objects.filter(email=email).exists() or Client.objects.filter(phone=phone).exists():
                    logger.info(f"📌 العميل {row['Name']} موجود مسبقًا.")
                    continue

                # ✅ إنشاء سجل جديد
                client = Client.objects.create(
                    name=row["Name"],
                    email=email,
                    phone=phone,
                    address=row.get("Address", ""),
                    client_source=row.get("Source", "other"),
                    status=row.get("Status", "potential"),
                    created_at=now()
                )
                new_clients.append(client)
                logger.info(f"✅ تم استيراد العميل {client.name} من Excel.")

            # 🔄 تشغيل تحليل الذكاء الاصطناعي بعد الاستيراد
            self.ai_analyzer.analyze_all_clients()
        except Exception as e:
            logger.error(f"❌ خطأ أثناء استيراد البيانات من Excel: {str(e)}")
        return new_clients


# ✅ تشغيل الاستيراد التلقائي عبر Celery كل 24 ساعة
def scheduled_client_import():
    importer = ClientAutoImporter()
    importer.import_from_social_media("Luxury Real Estate")
