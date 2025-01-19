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
    path('', home_view, name='home'),  # الصفحة الرئيسية
]
