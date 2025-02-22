import random
from django.db.models import Count, Q, Avg
from django.utils.timezone import now
from datetime import timedelta
from employees.models import Employee
from leads.models import Lead
import logging

# ✅ إعداد سجل الأخطاء لتسجيل المشاكل
logger = logging.getLogger(__name__)


def ai_select_best_employee():
    """
    ✅ اختيار الموظف المثالي لتوزيع العميل المحتمل بناءً على:
    - عدد العملاء المحتملين الحاليين لكل موظف.
    - تقييم الأداء التاريخي بناءً على معدلات التحويل.
    - توازن توزيع العملاء بين الموظفين.
    """
    employees = Employee.objects.annotate(
        leads_count=Count('leads'),
        conversion_rate=Avg('leads__status', filter=Q(leads__status="Converted"))
    ).order_by('leads_count', '-conversion_rate')  # ✅ الأولوية للموظفين الأقل ضغطًا والأعلى أداءً

    return employees.first() if employees.exists() else None


def distribute_leads():
    """
    ✅ توزيع الـ Leads غير المخصصة على الموظفين باستخدام الذكاء الصناعي.
    """
    # ✅ جلب جميع العملاء المحتملين الجدد الذين لم يتم تعيينهم بعد
    leads = Lead.objects.filter(status="New", assigned_to=None).order_by('-lead_score')  # ✅ ترتيب حسب الأولوية

    if not leads.exists():
        return "✅ No new leads to distribute."

    # ✅ جلب جميع الموظفين المتاحين
    employees = list(Employee.objects.all())
    employee_count = len(employees)

    if employee_count == 0:
        return "❌ No employees available for assignment."

    success_count = 0

    for lead in leads:
        # ✅ محاولة تعيين العميل المحتمل إلى أفضل موظف بناءً على الذكاء الصناعي
        assigned_employee = ai_select_best_employee()

        # ✅ إذا لم يتم العثور على موظف مثالي، استخدم `Round Robin`
        if not assigned_employee:
            assigned_employee = employees[success_count % employee_count]

        # ✅ تعيين العميل المحتمل للموظف المختار
        lead.assigned_to = assigned_employee
        lead.status = "In Progress"  # ✅ تحديث حالة العميل المحتمل
        lead.save()

        success_count += 1
        logger.info(f"🎯 Lead {lead.name} assigned to {assigned_employee.full_name}.")

    return f"✅ {success_count} leads distributed successfully."


def auto_reassign_stale_leads():
    """
    ✅ إعادة تعيين العملاء المحتملين الذين لم يتم التفاعل معهم خلال فترة معينة (7 أيام).
    """
    # ✅ البحث عن العملاء الذين لم يتم تحديثهم منذ 7 أيام
    stale_leads = Lead.objects.filter(status="In Progress", updated_at__lte=now() - timedelta(days=7))

    if not stale_leads.exists():
        return "✅ No stale leads found."

    reassigned_count = 0

    for lead in stale_leads:
        new_employee = ai_select_best_employee()

        if new_employee and new_employee != lead.assigned_to:
            logger.info(f"🔄 Reassigning {lead.name} from {lead.assigned_to} to {new_employee}.")
            lead.assigned_to = new_employee
            lead.save()
            reassigned_count += 1

    return f"✅ {reassigned_count} stale leads reassigned successfully."


def prioritize_leads():
    """
    ✅ تحديث مستوى الأولوية لكل Lead بناءً على عدة عوامل:
    - مستوى اهتمام العميل بالحملة.
    - البيانات السابقة الخاصة بالعميل (VIP، تكرار التفاعل).
    - مستوى الإنفاق المتوقع بناءً على تحليل AI.
    """
    for lead in Lead.objects.filter(status="New"):
        lead_score = random.randint(1, 100)  # 🔍 **محاكاة الذكاء الصناعي**
        lead.lead_score = lead_score
        lead.save()
        logger.info(f"⭐ Lead {lead.name} assigned a priority score of {lead_score}.")

    return "✅ Lead priorities updated."


def auto_lead_management():
    """
    ✅ إدارة العملاء المحتملين تلقائيًا عبر:
    - توزيع العملاء الجدد.
    - إعادة تعيين العملاء المهملين.
    - تحسين الأولويات.
    """
    print(distribute_leads())
    print(auto_reassign_stale_leads())
    print(prioritize_leads())


# ✅ **تشغيل النظام الذكي لإدارة العملاء المحتملين**
if __name__ == "__main__":
    auto_lead_management()
