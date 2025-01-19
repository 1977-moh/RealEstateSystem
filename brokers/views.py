from rest_framework import generics
from .models import Broker, BrokerClient, EmployeePerformance
from .serializers import BrokerSerializer, BrokerClientSerializer, EmployeePerformanceSerializer

class BrokerListCreateView(generics.ListCreateAPIView):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer


class BrokerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer


class BrokerClientListCreateView(generics.ListCreateAPIView):
    queryset = BrokerClient.objects.all()
    serializer_class = BrokerClientSerializer


class BrokerClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrokerClient.objects.all()
    serializer_class = BrokerClientSerializer


class EmployeePerformanceListCreateView(generics.ListCreateAPIView):
    queryset = EmployeePerformance.objects.all()
    serializer_class = EmployeePerformanceSerializer


class EmployeePerformanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmployeePerformance.objects.all()
    serializer_class = EmployeePerformanceSerializer
