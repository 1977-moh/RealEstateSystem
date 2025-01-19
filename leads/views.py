from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lead
from .serializers import LeadSerializer

class LeadListCreateView(APIView):
    """
    عرض لإرجاع قائمة الـ Leads أو إنشاء Lead جديد.
    """

    def get(self, request):
        """
        استرجاع جميع الـ Leads.
        """
        leads = Lead.objects.all()  # جلب جميع الـ Leads من قاعدة البيانات
        serializer = LeadSerializer(leads, many=True)  # تسلسل البيانات
        return Response(serializer.data, status=status.HTTP_200_OK)  # إرجاع البيانات مع حالة 200

    def post(self, request):
        """
        إنشاء Lead جديد.
        """
        serializer = LeadSerializer(data=request.data)  # تحميل بيانات الطلب
        if serializer.is_valid():  # التحقق من صحة البيانات
            serializer.save()  # حفظ الـ Lead الجديد في قاعدة البيانات
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # إرجاع بيانات الـ Lead الجديد
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # إرجاع الأخطاء في حال فشل التحقق
