from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .models import Property
from .serializers import PropertySerializer


class PropertyPagination(PageNumberPagination):
    """
    ✅ إعداد التصفح بحيث يكون عدد العقارات في الصفحة الواحدة 10.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class PropertyListView(generics.ListCreateAPIView):
    """
    ✅ عرض قائمة العقارات أو إنشاء عقار جديد.
    - دعم البحث والتصفية والفرز.
    - دعم التصفح (pagination).
    """
    queryset = Property.objects.all().order_by('-created_at')
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination

    # ✅ دعم البحث والتصفية والفرز
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'location', 'developer', 'payment_method']
    search_fields = ['property_type', 'location', 'developer', 'description']
    ordering_fields = ['price', 'created_at', 'delivery_date']

    def create(self, request, *args, **kwargs):
        """
        ✅ تخصيص عملية إنشاء عقار جديد مع منع التكرار.
        """
        location = request.data.get("location")
        developer = request.data.get("developer")

        if Property.objects.filter(location=location, developer=developer).exists():
            return Response({
                "message": "❌ A property with the same location and developer already exists."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            property_instance = serializer.save()
            return Response({
                "message": "✅ Property created successfully!",
                "property": PropertySerializer(property_instance).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    ✅ عرض تفاصيل العقار، تحديث، أو حذف.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    lookup_field = "id"

    def get_permissions(self):
        """
        ✅ السماح فقط للمشرفين بحذف العقارات.
        """
        if self.request.method == "DELETE":
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        """
        ✅ تخصيص عملية الحذف لتقديم استجابة مخصصة.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": f"❌ Property '{instance}' deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
