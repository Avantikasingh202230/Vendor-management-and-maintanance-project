# serializers.py

from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance
"""serializers for Vendor activities"""
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

""""serializers for purchase activities"""
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

""""serializers for storing performance matrix"""
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
