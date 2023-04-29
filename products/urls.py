"""cuFoodApp URL Configuration

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

app_name="products"

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('delete/<slug:slug>', views.delete_product, name="delete-product"),
    path('edit/<slug:slug>', views.edit_product, name="edit-product"),
    path('buy/order/<slug:slug>', views.order_product, name="order-product"),
    path('buy/<slug:slug>', views.buy_product, name="buy-product"),
    path('order-success/<slug:slug>/<slug:type>', views.order_success, name="order-success"),
    path('your-products', views.your_products, name="your-products"),
    path('seller-product/<slug:slug>', views.seller_product, name="seller-product"),
    path('add-product', views.add_product, name="add-product"),
    path('seller-orders', views.seller_orders, name="seller-orders"),
    path('seller-orders/mark-as-delivered/<slug:slug>', views.mark_as_delivered, name="mark-as-delivered"),
    path('seller-orders/mark-as-cancelled/<slug:slug>', views.mark_as_cancelled, name="mark-as-cancelled"),
    path('my-orders', views.my_orders, name="my-orders"),
    path('seller-order/info/<slug:orderID>', views.order_info, name="order-info"),
    path('page-not-found', views.invalid_request, name="page-not-found"),
]
