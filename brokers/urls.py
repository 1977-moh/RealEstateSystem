from django.urls import path
from .views import (
    BrokerListCreateView, BrokerDetailView,
    BrokerClientListCreateView, BrokerClientDetailView,
    EmployeePerformanceListCreateView, EmployeePerformanceDetailView,
    BrokerTransactionListCreateView, BrokerTransactionDetailView
)

# === 🔹 تحديد مساحة الأسماء لمنع التعارض ===
app_name = 'brokers'

urlpatterns = [
    # === 🏢 مسارات الوسطاء (Brokers) ===
    path('brokers/', BrokerListCreateView.as_view(), name='broker-list-create'),
    path('brokers/<uuid:pk>/', BrokerDetailView.as_view(), name='broker-detail'),

    # === 👥 مسارات العلاقات بين الوسطاء والعملاء (Broker-Clients) ===
    path('broker-clients/', BrokerClientListCreateView.as_view(), name='broker-client-list-create'),
    path('broker-clients/<uuid:pk>/', BrokerClientDetailView.as_view(), name='broker-client-detail'),

    # === 📊 مسارات تقييم أداء الموظفين (Employee Performance) ===
    path('employee-performance/', EmployeePerformanceListCreateView.as_view(), name='employee-performance-list-create'),
    path('employee-performance/<uuid:pk>/', EmployeePerformanceDetailView.as_view(), name='employee-performance-detail'),

    # === 💰 مسارات معاملات الوسطاء المالية (Broker Transactions) ===
    path('broker-transactions/', BrokerTransactionListCreateView.as_view(), name='broker-transaction-list-create'),
    path('broker-transactions/<uuid:pk>/', BrokerTransactionDetailView.as_view(), name='broker-transaction-detail'),
]
