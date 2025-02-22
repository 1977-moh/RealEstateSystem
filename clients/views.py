from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from datetime import date, timedelta
from .models import Client


class ClientFollowUpView(APIView):
    """
    ✅ API لمتابعة العملاء وتحليل البيانات الذكية.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        ✅ البحث عن العملاء الذين يجب متابعتهم.
        """
        today = date.today()
        upcoming_followups = Client.objects.filter(follow_up_date__lte=today + timedelta(days=7)).order_by('follow_up_date')

        # ✅ تصنيف العملاء بناءً على احتمالية الشراء
        high_potential_clients = Client.objects.filter(predicted_interest_score__gte=75)

        data = {
            "follow_up_clients": list(upcoming_followups.values('name', 'email', 'phone', 'status', 'follow_up_date')),
            "high_potential_clients": list(high_potential_clients.values('name', 'email', 'predicted_interest_score'))
        }

        return Response(data, status=status.HTTP_200_OK)
