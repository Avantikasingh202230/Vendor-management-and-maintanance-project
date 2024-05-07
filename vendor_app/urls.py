# urls.py
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from .views import (
    VendorCreateAPIView,
    VendorListAPIView,
    VendorRetrieveAPIView,
    VendorUpdateAPIView,
    VendorDestroyAPIView,
)
from .views import (
    PurchaseOrderListCreateAPIView,PurchaseOrderListAPIView,
    PurchaseOrderRetrieveAPIView,
    PurchaseOrderUpdateAPIView,
    PurchaseOrderDestroyAPIView, VendorPerformanceAPIView,login
)

urlpatterns = [
    #logi functionality for jwt authentication to secure all the API'S
    path('api/login/', login, name='api-login'),
    
    #Create a new user 
    path('api/vendors/create/', VendorCreateAPIView.as_view(), name='vendor-create'),
    #List  all the vendor 
    path('api/vendors/', VendorListAPIView.as_view(), name='vendor-list'),
    # Retrieve a specific vendor's details
    path('api/vendors/<int:pk>/', VendorRetrieveAPIView.as_view(), name='vendor-retrieve'),
    #Update a vendor's details 
    path('api/vendors/<int:pk>/update/', VendorUpdateAPIView.as_view(), name='vendor-update'),
    #Delete a vendor 
    path('api/vendors/<int:pk>/delete/', VendorDestroyAPIView.as_view(), name='vendor-delete'),

    #Create a purchase order 
    path('api/purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase_order_list_create'),
    #List all the purchase orders with an option to filter by vendor 
    path('api/purchase_orders/all/', PurchaseOrderListAPIView.as_view(), name='purchase_order_list_all'),  # Define the new URL pattern
    #Retrieve details of specific purchase order
    path('api/purchase_orders/<int:pk>/', PurchaseOrderRetrieveAPIView.as_view(), name='purchase_order_retrieve'),
    #Update a purchase order 
    path('api/purchase_orders/<int:pk>/update/', PurchaseOrderUpdateAPIView.as_view(), name='purchase_order_update'),
    #Delete  a purchase order
    path('api/purchase_orders/<int:pk>/delete/', PurchaseOrderDestroyAPIView.as_view(), name='purchase_order_delete'),
    
    
    
    #Retrieve a vendor's performance matrix"""
    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
]
