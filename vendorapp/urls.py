"""vendor_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create_vendor/',views.CreateVendorView.as_view(),name='create_vendor'),
    path('vendors/',views.getall_vendor_view,name= 'get_vendors'),
    path('vendors/<str:vendor_id>/',views.Vender_view.as_view(),name='get_vendor'),
    path('purchase_orders/',views.CreatePurchaseView.as_view(),name='purchase_orders'),
    path('purchase_orders/',views.getall_purchase_view,name= 'purchase_orders'),
    path('purchase_orders/<str:po_id>/',views.Vender_view.as_view(),name='purchase'),
    path('api/vendors/<int:vendor_id>/performance/', views.vendor_performance_view, name='vendor_performance'),
]
