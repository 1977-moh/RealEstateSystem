from django.contrib import admin
from django.urls import path, include
from home.views import home_view  # استيراد العرض (view) للصفحة الرئيسية

urlpatterns = [
    path('admin/', admin.site.urls),  # رابط لوحة التحكم
    path('api/clients/', include('clients.urls')),  # رابط تطبيق العملاء
    path('api/properties/', include('properties.urls')),  # رابط تطبيق العقارات
    path('api/employees/', include('employees.urls')),  # رابط تطبيق الموظفين
    path('api/campaigns/', include('campaigns.urls')),  # رابط تطبيق الحملات الإعلانية
    path('api/leads/', include('leads.urls')),  # رابط تطبيق الليدز
    path('api/payments/', include('payments.urls')),  # رابط تطبيق الدفع
    path('api/', include('offer.urls')),
    path('', home_view, name='home'),  # الصفحة الرئيسية
]

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Real Estate System API",
        default_version='v1',
        description="Documentation for all API endpoints",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
