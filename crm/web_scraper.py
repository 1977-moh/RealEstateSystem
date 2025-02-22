import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from .social_accounts import load_accounts


class SocialMediaScraper:
    """
    ✅ أداة البحث المتقدمة عن العملاء المحتملين من وسائل التواصل الاجتماعي.
    """

    def __init__(self):
        self.accounts = load_accounts()

    def search_google(self, keyword):
        """
        ✅ البحث في Google عن العملاء المحتملين.
        """
        print(f"🔍 البحث عن '{keyword}' في Google...")
        search_url = f"https://www.google.com/search?q={quote(keyword)}+real+estate+clients"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            results = []
            for a in soup.select("h3"):
                link = a.find_parent("a")
                if link and link.get("href"):
                    results.append({"title": a.text, "link": link["href"]})

            return results[:5]  # ✅ استرجاع أول 5 نتائج فقط

        except requests.exceptions.RequestException as e:
            print(f"⚠️ خطأ في الاتصال بـ Google: {e}")
            return []

    def search_social_media(self, platform, keyword):
        """
        ✅ البحث في منصة تواصل اجتماعي معينة.
        """
        if platform not in self.accounts:
            print(f"⚠️ لم يتم العثور على حساب {platform.capitalize()}. الرجاء إضافته.")
            return []

        print(f"🔍 البحث عن '{keyword}' في {platform.capitalize()}...")
        return [{"platform": platform, "keyword": keyword, "message": f"نتائج البحث عن {keyword}"}]

    def search_all(self, keyword):
        """
        ✅ البحث في جميع المنصات المتاحة.
        """
        results = []
        results.extend(self.search_google(keyword))

        platforms = ["facebook", "linkedin", "tiktok", "instagram"]
        for platform in platforms:
            results.extend(self.search_social_media(platform, keyword))

        return results


# ✅ إضافة دالة `fetch_potential_clients` لاستدعاء البحث عن العملاء المحتملين
def fetch_potential_clients(keyword):
    """
    ✅ البحث عن العملاء المحتملين في وسائل التواصل الاجتماعي و Google.
    """
    scraper = SocialMediaScraper()
    potential_clients = scraper.search_all(keyword)
    return potential_clients


# 🌟 **مثال استخدام**:
# leads = fetch_potential_clients("Luxury Apartments in Dubai")
# print(leads)
