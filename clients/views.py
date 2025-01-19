from rest_framework import generics, permissions
from .models import Client
from .serializers import ClientSerializer

class ClientListView(generics.ListCreateAPIView):
    """
    عرض لإرجاع قائمة العملاء أو إنشاء عميل جديد.
    """
    queryset = Client.objects.all().order_by('-created_at')  # ترتيب السجلات الأحدث أولاً
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح للمستخدمين المصادق عليهم فقط

    def get_queryset(self):
        """
        تخصيص البيانات التي يتم إرجاعها بناءً على البحث أو التصفية.
        """
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)  # البحث
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض لتفاصيل العميل، تحديث، أو حذف.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]  # السماح للمستخدمين المصادق عليهم فقط

    def perform_update(self, serializer):
        """
        تخصيص عملية التحديث.
        """
        serializer.save(updated_at=self.request.user)
