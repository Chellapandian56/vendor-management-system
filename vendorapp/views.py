from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view
from .models import Vendor,PurchaseOrder
from rest_framework import status
from rest_framework.views import APIView,Response
from vendorapp.serializers import VendorSerializer,PurchaseSerializer,VendorPerformanceSerializer
from django.shortcuts import get_object_or_404
# import requests

# Create your views here.


class CreateVendorView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          serialized_data = serializer.data
          response_data = {
              "message": "Vendor created successfully",
              "vendor": serialized_data
          }
          return Response(response_data, status=status.HTTP_201_CREATED)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["POST"])
# def vendor_create_view(request):
#   name = request.data.get("name")
#   address = request.data.get("address")
#   contact_details = request.data.get("contact_details")
#   data = Vendor.objects.create(name  = name ,address = address, contact_details = contact_details)
#   return Response({"success":"success"})


@api_view(["GET"])
def getall_vendor_view(request):
  # name = request.data.get("vendor_id")
  data = Vendor.objects.all().values()
  print(data)
  return Response({"status":"success","data":data})



class Vender_view(APIView):
  def get(self,request,vendor_id):
    data = Vendor.objects.filter(vendor_code = vendor_id).values()
    return Response({"status":"success","data":data})
  
  def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
  
  def delete(self,request,vendor_id):
    try:
        vendor = Vendor.objects.get(vendor_code=vendor_id)
        vendor.delete()
        return Response({"status": "success"})
    except  Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)



class CreatePurchaseView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseSerializer
    def post(self, request):
      serializer = self.serializer_class(data=request.data)
      if serializer.is_valid():
          serializer.save()
          serialized_data = serializer.data
          response_data = {
              "message": "Order created successfully",
              "vendor": serialized_data
          }
          return Response(response_data, status=status.HTTP_201_CREATED)
      else:
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET"])
def getall_purchase_view(request):
  data = PurchaseOrder.objects.all().values()
  return Response({"status":"success","data":data})



class Purchase_view(APIView):
  def get(self,request,po_id):
    data = PurchaseOrder.objects.filter(po_number= po_id).values()
    return Response({"status":"success","data":data})
  
  def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
  
  def delete(self,request,po_id):
    try:
        purchase_order = PurchaseOrder.objects.get(po_number= po_id)
        purchase_order.delete()
        return Response({"status": "success"})
    except  PurchaseOrder.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET"])
def getall_purchase_view(request):
  data = PurchaseOrder.objects.all().values()
  return Response({"status":"success","data":data})


@api_view(['GET'])
def vendor_performance_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    serializer = VendorPerformanceSerializer(vendor)
    return Response({"status":"success","data":serializer.data})