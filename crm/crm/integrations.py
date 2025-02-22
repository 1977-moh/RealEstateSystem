from employees.models import Employee
from campaigns.models import Campaign

def assign_employee_to_client(client):
    """
    ✅ تعيين موظف تلقائيًا لمتابعة العميل
    """
    employees = Employee.objects.all()
    if employees.exists():
        client.assigned_employee = employees.order_by('?').first()
        client.save()

def link_client_to_campaign(client, campaign_id):
    """
    ✅ ربط العميل بحملة إعلانية
    """
    campaign = Campaign.objects.filter(id=campaign_id).first()
    if campaign:
        client.campaign = campaign
        client.save()
