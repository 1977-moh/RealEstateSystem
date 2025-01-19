from django.urls import path
from .views import (
    BrokerListCreateView, BrokerDetailView,
    BrokerClientListCreateView, BrokerClientDetailView,
    EmployeePerformanceListCreateView, EmployeePerformanceDetailView
)

urlpatterns = [
    path('brokers/', BrokerListCreateView.as_view(), name='broker-list'),
    path('brokers/<int:pk>/', BrokerDetailView.as_view(), name='broker-detail'),
    path('broker-clients/', BrokerClientListCreateView.as_view(), name='broker-client-list'),
    path('broker-clients/<int:pk>/', BrokerClientDetailView.as_view(), name='broker-client-detail'),
    path('employee-performance/', EmployeePerformanceListCreateView.as_view(), name='employee-performance-list'),
    path('employee-performance/<int:pk>/', EmployeePerformanceDetailView.as_view(), name='employee-performance-detail'),
]
