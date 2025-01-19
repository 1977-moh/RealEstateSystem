from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Property
from .serializers import PropertySerializer


class PropertyListView(generics.ListCreateAPIView):
    """
    عرض لإرجاع قائمة العقارات أو إنشاء عقار جديد.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_queryset(self):
        """
        السماح بالتصفية بناءً على نوع العقار أو الموقع.
        """
        queryset = super().get_queryset()
        property_type = self.request.query_params.get('property_type')
        location = self.request.query_params.get('location')
        if property_type:
            queryset = queryset.filter(property_type=property_type)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

    def create(self, request, *args, **kwargs):
        """
        تخصيص عملية إنشاء عقار جديد لتقديم استجابة مخصصة.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Property created successfully!",
                "property": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    عرض لتفاصيل العقار، تحديث، أو حذف.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def destroy(self, request, *args, **kwargs):
        """
        تخصيص عملية الحذف لتقديم استجابة مخصصة.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message": f"Property '{instance}' deleted successfully."
        }, status=status.HTTP_204_NO_CONTENT)
