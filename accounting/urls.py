from django.urls import path
from .views import (
    SalaryListCreateView, SalaryDetailView,
    BonusListCreateView, BonusDetailView,
    DeductionListCreateView, DeductionDetailView,
    SalesCommissionListCreateView, SalesCommissionDetailView
)

# ✅ تحديد اسم التطبيق لتجنب التعارض مع التطبيقات الأخرى
app_name = 'accounting'

urlpatterns = [
    # ✅ مسارات إدارة المرتبات (Salaries)
    path('salaries/', SalaryListCreateView.as_view(), name='salary-list-create'),
    path('salaries/<int:pk>/', SalaryDetailView.as_view(), name='salary-detail'),

    # ✅ مسارات إدارة المكافآت (Bonuses)
    path('bonuses/', BonusListCreateView.as_view(), name='bonus-list-create'),
    path('bonuses/<int:pk>/', BonusDetailView.as_view(), name='bonus-detail'),

    # ✅ مسارات إدارة الخصومات (Deductions)
    path('deductions/', DeductionListCreateView.as_view(), name='deduction-list-create'),
    path('deductions/<int:pk>/', DeductionDetailView.as_view(), name='deduction-detail'),

    # ✅ مسارات إدارة العمولات (Sales Commissions)
    path('commissions/', SalesCommissionListCreateView.as_view(), name='commission-list-create'),
    path('commissions/<int:pk>/', SalesCommissionDetailView.as_view(), name='commission-detail'),
]
