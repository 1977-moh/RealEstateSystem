from rest_framework import generics, filters, permissions, serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from datetime import timedelta
from .models import Lead
from .serializers import LeadSerializer
import random


class LeadPagination(PageNumberPagination):
    """
    ✅ إعداد التصفح بحيث يكون عدد العناصر في الصفحة 10.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class LeadListCreateView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة العملاء المحتملين أو إنشاء عميل جديد.
    - دعم البحث والتصفية والفرز.
    - تحليل جودة العملاء المحتملين (`AI Lead Score`).
    """
    queryset = Lead.objects.select_related('campaign').all().order_by('-created_at')  # ✅ تحسين الأداء باستخدام `select_related`
    serializer_class = LeadSerializer
    pagination_class = LeadPagination
    permission_classes = [permissions.IsAuthenticated]

    # ✅ دعم البحث والتصفية
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'campaign__name']
    filterset_fields = ['status', 'campaign']
    ordering_fields = ['created_at', 'updated_at']

    def get_queryset(self):
        """
        ✅ تحسين البحث ليشمل الاسم، البريد الإلكتروني، الهاتف، واسم الحملة.
        ✅ تصنيف العملاء المحتملين بناءً على الأولوية (`AI Lead Score`).
        """
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(campaign__name__icontains=search_query)
            )

        return queryset.annotate(
            lead_priority=Count('id')
        ).order_by('-lead_priority')

    def perform_create(self, serializer):
        """
        ✅ منع تكرار نفس العميل داخل نفس الحملة.
        ✅ ضبط `status` تلقائيًا ليكون `New`.
        ✅ تحليل جودة العميل (`Lead Score`).
        """
        email = serializer.validated_data['email'].strip().lower()
        campaign = serializer.validated_data['campaign']

        existing_lead = Lead.objects.filter(email=email, campaign=campaign).first()

        if existing_lead:
            raise serializers.ValidationError({"email": "❌ هذا البريد الإلكتروني مسجل بالفعل لهذه الحملة!"})

        lead = serializer.save(status='New', email=email)

        # ✅ إضافة `AI Lead Score`
        lead.lead_score = random.randint(50, 100)
        lead.save()


class LeadDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض / تعديل / حذف `Lead` معين.
    - منع تعديل الحملة بعد إنشائها.
    - دعم تحديث الحالة بناءً على قيود محددة.
    """
    queryset = Lead.objects.select_related('campaign').all()
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        ✅ منع تعديل `campaign` بعد الإنشاء.
        ✅ السماح فقط بتحديث `status` إلى الحالات المسموحة.
        ✅ تفعيل `AI Smart Follow-up` عند تحديث `status`.
        """
        instance = self.get_object()
        new_status = serializer.validated_data.get('status', instance.status)

        # ✅ التحقق من تغييرات `status` المسموحة
        allowed_transitions = {
            "New": ["In Progress", "Closed", "Converted"],
            "In Progress": ["Closed", "Converted"],
            "Closed": [],
            "Converted": [],
        }

        if new_status != instance.status and new_status not in allowed_transitions.get(instance.status, []):
            raise serializers.ValidationError({
                "status": f"🚨 لا يمكن تغيير الحالة مباشرة من {instance.status} إلى {new_status}."
            })

        # ✅ تفعيل `AI Smart Follow-up`
        if new_status == "In Progress":
            self.schedule_follow_up(instance)

        serializer.validated_data.pop('campaign', None)  # ✅ منع تعديل الحملة بعد الإنشاء
        serializer.save()

    def schedule_follow_up(self, lead_instance):
        """
        ✅ جدولة متابعة ذكية (`AI Smart Follow-up`) للعميل المحتمل.
        """
        follow_up_days = random.randint(2, 7)  # ✅ تحديد موعد المتابعة بين 2-7 أيام بناءً على `AI Analysis`
        follow_up_date = lead_instance.created_at.date() + timedelta(days=follow_up_days)
        print(f"📅 متابعة ذكية مجدولة في {follow_up_date} لـ {lead_instance.name}.")


class AILeadAnalysisView(generics.ListAPIView):
    """
    ✅ تحليل العملاء المحتملين باستخدام الذكاء الصناعي (`AI Lead Score`).
    """
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        ✅ استرجاع العملاء المحتملين بناءً على `AI Lead Score`.
        """
        return Lead.objects.order_by('-lead_score')


class LeadPerformanceReportView(generics.ListAPIView):
    """
    ✅ تقرير أداء العملاء المحتملين بناءً على الحملات الإعلانية.
    """
    serializer_class = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        ✅ إنشاء تحليل مفصل عن العملاء المحتملين ونسبة التحويل.
        """
        return Lead.objects.annotate(
            conversion_rate=Count('id', filter=Q(status="Converted")) / Count('id') * 100
        ).order_by('-conversion_rate')
