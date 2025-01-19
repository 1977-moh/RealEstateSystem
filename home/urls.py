from django.urls import path
from .views import home_view

# تعريف مسارات تطبيق home
urlpatterns = [
    path('', home_view, name='home'),  # الصفحة الرئيسية للتطبيق
]
