import os
import shutil

# 🔍 تحديد المسار الرئيسي لمجلد الـ CRM
crm_main = os.path.join(os.getcwd(), "crm")  # crm الرئيسي
crm_nested = os.path.join(crm_main, "crm")   # crm داخل crm

# ✅ التحقق من وجود المجلد الداخلي قبل النقل
if os.path.exists(crm_nested):
    # 🔄 نقل جميع الملفات من `crm/crm/` إلى `crm/`
    for file_name in os.listdir(crm_nested):
        source = os.path.join(crm_nested, file_name)
        destination = os.path.join(crm_main, file_name)

        # 🚀 النقل الفعلي للملفات والمجلدات
        shutil.move(source, destination)
        print(f"✅ تم نقل {file_name} إلى {crm_main}")

    # 🗑️ حذف المجلد الفارغ `crm/crm/`
    os.rmdir(crm_nested)
    print(f"🚮 تم حذف المجلد الفارغ: {crm_nested}")

else:
    print("🎯 لا يوجد تكرار في المجلدات. لا حاجة للنقل!")


