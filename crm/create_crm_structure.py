import os

# 🔹 تحديد المسار الصحيح لمجلد CRM
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # تحديد مسار المشروع الأساسي
CRM_DIR = os.path.join(BASE_DIR, "crm")  # تحديد مسار crm

# 🔹 قائمة الملفات والمجلدات المطلوبة داخل crm
crm_structure = [
    "__init__.py",  # ملف تعريف Django App
    "models.py",  # نماذج قاعدة البيانات
    "serializers.py",  # تحويل البيانات إلى JSON
    "views.py",  # تنفيذ عمليات CRM
    "urls.py",  # تعريف المسارات API
    "web_scraper.py",  # البحث الذكي عن العملاء المحتملين
    "client_auto_import.py",  # إدخال البيانات تلقائيًا
    "ai_analyzer.py",  # تحليل العملاء بالذكاء الصناعي
    "client_offers.py",  # إرسال العروض الذكية
    "tasks.py",  # جدولة المهام التلقائية
    "integrations.py",  # ربط CRM مع الموظفين والحملات
    "notifications.py",  # إرسال التنبيهات عبر البريد وواتساب
    "admin.py",  # إدارة العملاء من لوحة تحكم Django
    "apps.py",  # تعريف التطبيق داخل Django
    "signals.py",  # تشغيل عمليات تلقائية عند تعديل العملاء
    "tests.py",  # الاختبارات
]

# 🔹 إنشاء المجلد `crm` إذا لم يكن موجودًا
if not os.path.exists(CRM_DIR):
    os.makedirs(CRM_DIR)

# 🔹 إنشاء الملفات داخل `crm`
for file in crm_structure:
    file_path = os.path.join(CRM_DIR, file)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {file} - Generated\n")

# 🔹 إنشاء مجلد `migrations` بشكل صحيح
migrations_dir = os.path.join(CRM_DIR, "migrations")
os.makedirs(migrations_dir, exist_ok=True)

# 🔹 إنشاء ملف `__init__.py` داخل `migrations`
migrations_init_file = os.path.join(migrations_dir, "__init__.py")
if not os.path.exists(migrations_init_file):
    with open(migrations_init_file, "w", encoding="utf-8") as f:
        f.write("# Migrations folder for CRM\n")

print("✅ CRM structure created successfully with correct paths!")
