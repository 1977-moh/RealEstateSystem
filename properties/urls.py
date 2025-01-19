from django.urls import path
from .views import PropertyListView, PropertyDetailView

# تعريف مساحة أسماء للتطبيق
app_name = 'properties'

urlpatterns = [
    # عرض قائمة العقارات
    path('', PropertyListView.as_view(), name='list'),

    # عرض تفاصيل العقار بناءً على المفتاح الأساسي
    path('<int:pk>/', PropertyDetailView.as_view(), name='detail'),
]
