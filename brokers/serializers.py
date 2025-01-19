from rest_framework import serializers
from .models import Broker, BrokerClient, EmployeePerformance

class BrokerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broker
        fields = '__all__'


class BrokerClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerClient
        fields = '__all__'


class EmployeePerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePerformance
        fields = '__all__'
