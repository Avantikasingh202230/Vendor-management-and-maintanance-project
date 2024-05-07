from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Vendor, PurchaseOrder,HistoricalPerformance
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
""""  Vendor profile Management  """


# Create a new user 
class VendorCreateAPIView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
#List  all the vendor 
class VendorListAPIView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
# Retrieve a specific vendor's details
class VendorRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
#Update a vendor's details 
class VendorUpdateAPIView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
#Delete a vendor 
class VendorDestroyAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    authentication_classes = [JWTAuthentication]
    
 

""""Purchase Order Tracking """

#Create a purchase order     
class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]

 #List all the purchase orders with an option to filter by vendor 
class PurchaseOrderListAPIView(generics.ListAPIView):
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        vendor_id = self.request.query_params.get('vendor_id')
        print(vendor_id)
        if vendor_id:
            # Filter purchase orders by vendor ID
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

#Retrieve a pecific Purchase order data 
class PurchaseOrderRetrieveAPIView(generics.RetrieveAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]

#Update a purchase order 
class PurchaseOrderUpdateAPIView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]

#Delete  a purchase order
class PurchaseOrderDestroyAPIView(generics.DestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    authentication_classes = [JWTAuthentication]



""""Vendor Performance Evaluation"""

 #Retrieve a vendor's performance matrix"""
class VendorPerformanceAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request, vendor_id):
        try:
            # Retrieve historical performance data for the vendor
            performance_data = HistoricalPerformance.objects.filter(vendor_id=vendor_id)
            serializer = HistoricalPerformanceSerializer(performance_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except HistoricalPerformance.DoesNotExist:
            return Response({"error": "Performance data not found for the vendor"}, status=status.HTTP_404_NOT_FOUND)

#jwt authentication 
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        vendor_code = request.data.get('vendor_code')
        print("the vendor_code",vendor_code)
        # Retrieve all vendor codes from the Vendor table
        all_vendor_codes = Vendor.objects.values_list('vendor_code', flat=True)
        print(all_vendor_codes)
        # Check if the provided vendor_code is in the list of all_vendor_codes
        if vendor_code in all_vendor_codes:
            # If the vendor_code matches, retrieve the vendor object
            vendor = get_object_or_404(Vendor, vendor_code=vendor_code)
            print(type(vendor))
            refresh = RefreshToken()
            print(refresh)
            return Response({'refresh': str(refresh)})
        else:
            # If the vendor_code does not match any in the database, return an error
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)




