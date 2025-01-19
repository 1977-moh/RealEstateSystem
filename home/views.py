from django.shortcuts import render
from django.template.loader import get_template


def home_view(request):
    """
    عرض الصفحة الرئيسية.
    """
    # اختبار مسار القالب (يمكن استخدامه أثناء التصحيح فقط)
    try:
        template = get_template('home/index.html')  # الحصول على القالب
        print(f"Template found: {template.origin.name}")  # طباعة مسار القالب
    except Exception as e:
        print(f"Error finding template: {e}")  # طباعة الخطأ إن وجد

    # إعادة عرض الصفحة الرئيسية
    return render(request, 'home/index.html')
