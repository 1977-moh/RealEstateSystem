from employees.models import Employee
from .models import Lead

def distribute_leads():
    """
    وظيفة لتوزيع الـ Leads غير المخصصة على الموظفين المتاحين.
    """
    # جلب جميع الـ Leads الجديدة التي لم يتم تعيينها بعد
    leads = Lead.objects.filter(status="New", assigned_to=None)

    # جلب جميع الموظفين
    employees = Employee.objects.all()
    employee_count = employees.count()

    # التحقق من وجود موظفين
    if employee_count == 0:
        return "No employees available for assignment."

    # توزيع الـ Leads بالتساوي بين الموظفين
    for index, lead in enumerate(leads):
        assigned_employee = employees[index % employee_count]  # التوزيع بالتناوب (Round Robin)
        lead.assigned_to = assigned_employee
        lead.status = "In Progress"  # تحديث حالة الـ Lead إلى "In Progress"
        lead.save()

    return f"{leads.count()} leads distributed successfully."
