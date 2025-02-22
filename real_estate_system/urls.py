from django.contrib import admin
from django.urls import path, include, re_path
from home.views import HomeView  # ✅ تصحيح الاستيراد
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

# === 📝 إعداد توثيق API باستخدام Swagger & Spectacular ===
schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate System API",
        default_version='v1',
        description="Comprehensive API Documentation for the Real Estate Management System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],  # ✅ جعل التوثيق متاحًا للجميع
)

# === 🏗️ تنظيم مسارات API داخل `api/` ===
api_patterns = [
    path('clients/', include('clients.urls', namespace='clients')),
    path('properties/', include('properties.urls', namespace='properties')),
    path('employees/', include('employees.urls', namespace='employees')),
    path('campaigns/', include('campaigns.urls', namespace='campaigns')),
    path('leads/', include('leads.urls', namespace='leads')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('offers/', include('offer.urls', namespace='offer')),  # ✅ تصحيح الاسم `offers`
    path('brokers/', include('brokers.urls', namespace='brokers')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),  # ✅ جعل جميع API تحت `api/`
    path('', HomeView.as_view(), name='home'),  # ✅ تصحيح `HomeView`

    # ✅ توثيق API باستخدام Swagger و ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # ✅ إضافة دعم `drf-spectacular`
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # ✅ تصحيح مسار CRM (قد تحتاج إلى تعديل المسار حسب المشكلة)
    path('crm/', include('crm.crm.urls', namespace='crm')),  # ✅ تأكد من المسار الصحيح
]
