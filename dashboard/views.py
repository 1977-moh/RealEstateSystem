from rest_framework import generics, permissions
from django.db.models import Sum, Count
from clients.models import Client
from properties.models import Property
from payments.models import Payment
from campaigns.models import Campaign
from .models import DashboardStats
from .serializers import DashboardStatsSerializer


class DashboardView(generics.RetrieveAPIView):
    """
    ✅ عرض الإحصائيات في الـ Dashboard، يتم تحديث البيانات تلقائيًا عند الاستدعاء.
    """
    queryset = DashboardStats.objects.all().order_by('-last_updated')
    serializer_class = DashboardStatsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        ✅ تحديث البيانات تلقائيًا عند كل طلب.
        """
        obj, created = DashboardStats.objects.get_or_create()

        # تحديث القيم من قواعد البيانات
        obj.total_clients = Client.objects.count()
        obj.total_properties = Property.objects.count()
        obj.total_sales = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0.0
        obj.active_campaigns = Campaign.objects.filter(status="Active").count()
        obj.save()

        return obj
