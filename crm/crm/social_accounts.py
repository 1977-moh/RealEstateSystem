import json
import os

SOCIAL_ACCOUNTS_FILE = "social_accounts.json"

def load_accounts():
    """
    ✅ تحميل الحسابات المسجلة من ملف JSON.
    """
    if os.path.exists(SOCIAL_ACCOUNTS_FILE):
        with open(SOCIAL_ACCOUNTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_accounts(accounts):
    """
    ✅ حفظ الحسابات إلى ملف JSON.
    """
    with open(SOCIAL_ACCOUNTS_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)

def add_account(platform, username, password, api_key=None):
    """
    ✅ إضافة حساب جديد.
    """
    accounts = load_accounts()
    accounts[platform] = {
        "username": username,
        "password": password,
        "api_key": api_key
    }
    save_accounts(accounts)
    print(f"✅ تم حفظ حساب {platform} بنجاح!")

def remove_account(platform):
    """
    ✅ حذف حساب معين.
    """
    accounts = load_accounts()
    if platform in accounts:
        del accounts[platform]
        save_accounts(accounts)
        print(f"❌ تم حذف حساب {platform}.")
    else:
        print(f"⚠️ الحساب غير موجود!")

def list_accounts():
    """
    ✅ عرض الحسابات المسجلة.
    """
    accounts = load_accounts()
    if accounts:
        for platform, details in accounts.items():
            print(f"🔹 {platform}: {details['username']}")
    else:
        print("⚠️ لا توجد حسابات مسجلة بعد!")

# 🌟 مثال استخدام:
# add_account("facebook", "user@example.com", "securepassword123", "API_KEY_HERE")
# list_accounts()
