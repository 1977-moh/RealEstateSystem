import pandas as pd
from datetime import timedelta
from employees.models import Employee
from leads.models import Lead
from django.utils.timezone import now
import logging

# ✅ إعداد سجل الأخطاء لتسجيل المشاكل
logger = logging.getLogger(__name__)


def generate_lead_performance_report():
    """
    ✅ تحليل أداء موظفي المبيعات بناءً على عدد الـ Leads وتحويلهم إلى عملاء.
    """
    report = []
    total_leads_all = Lead.objects.count() or 1  # تجنب القسمة على الصفر

    for employee in Employee.objects.all():
        # 🔹 جلب بيانات الـ Leads لكل موظف
        total_leads = Lead.objects.filter(assigned_to=employee).count()
        converted_leads = Lead.objects.filter(assigned_to=employee, status="Converted").count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

        # 🔹 تحليل أداء الموظف مقارنة بالمتوسط العام
        avg_conversion_rate = (converted_leads / total_leads_all * 100)

        # 🧠 **تحليل الذكاء الصناعي**: اقتراح تحسينات
        performance_insight = analyze_employee_performance(employee, conversion_rate)

        report.append({
            "employee": employee.full_name,
            "total_leads": total_leads,
            "converted_leads": converted_leads,
            "conversion_rate": f"{conversion_rate:.2f}%",
            "average_conversion_rate": f"{avg_conversion_rate:.2f}%",
            "performance_insight": performance_insight,
        })

    # 📊 **تحويل التقرير إلى DataFrame لسهولة التحليل**
    df = pd.DataFrame(report)
    return df


def analyze_employee_performance(employee, conversion_rate):
    """
    ✅ تحليل ذكاء صناعي لتقييم أداء الموظف.
    """
    performance_tips = []

    # 🔹 مقارنة الأداء بالمعدل العام
    if conversion_rate < 10:
        performance_tips.append("🚨 أداء منخفض، يُفضل إعادة تدريب الموظف.")
    elif 10 <= conversion_rate < 30:
        performance_tips.append("⚠️ أداء مقبول ولكن يمكن تحسينه بالمتابعة الدورية.")
    else:
        performance_tips.append("✅ أداء ممتاز، يُنصح بتحفيز الموظف بمكافآت.")

    # 🔹 تحليل التغيير في الأداء خلال 3 أشهر
    three_months_ago = now() - timedelta(days=90)
    past_leads = Lead.objects.filter(assigned_to=employee, created_at__gte=three_months_ago).count()

    if past_leads < 5:
        performance_tips.append("📉 نشاط ضعيف في الأشهر الأخيرة، يُفضل زيادة التفاعل مع العملاء.")

    return " | ".join(performance_tips)


def redistribute_leads():
    """
    ✅ إعادة توزيع العملاء المحتملين تلقائيًا إذا كان أداء الموظف ضعيفًا.
    """
    low_performers = []
    employees = Employee.objects.all()

    for employee in employees:
        total_leads = Lead.objects.filter(assigned_to=employee).count()
        converted_leads = Lead.objects.filter(assigned_to=employee, status="Converted").count()
        conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0

        if conversion_rate < 10:
            low_performers.append(employee)

    if low_performers:
        # 🔹 إعادة توزيع العملاء المحتملين على الموظفين ذوي الأداء الأفضل
        high_performers = [e for e in employees if e not in low_performers]

        for lead in Lead.objects.filter(status="New", assigned_to__in=low_performers):
            best_employee = min(high_performers, key=lambda emp: Lead.objects.filter(assigned_to=emp).count())
            lead.assigned_to = best_employee
            lead.save()

        return f"✅ تمت إعادة توزيع {len(low_performers)} موظفين ذوي أداء منخفض."

    return "📌 لا حاجة لإعادة توزيع العملاء."


def print_lead_performance():
    """
    ✅ طباعة تقرير أداء الموظفين في لوحة الإدارة.
    """
    df = generate_lead_performance_report()
    print(df.to_string(index=False))  # 📊 طباعة البيانات بشكل جدول مرتب

    # ✅ حفظ التقرير في ملف JSON لتحليله لاحقًا
    df.to_json("lead_performance_report.json", orient="records", indent=4)
    print("📁 تم حفظ التقرير في 'lead_performance_report.json'")


# ✅ **تشغيل التقرير**
if __name__ == "__main__":
    print_lead_performance()
    print(redistribute_leads())
