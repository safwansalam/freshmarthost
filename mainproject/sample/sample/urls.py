"""
URL configuration for sample project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from app1 import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('admin_home',views.admin_home),
    path('user_home',views.user_home),
    path('add_product',views.add_product),
    path('manage_product',views.manage_product),
    path('delete_product/<int:d>',views.delete_product),
    path('update_product/<int:d>',views.update_product),
    path('subscription',views.subscription),
    path('add_plan',views.add_plan),
    path('subscribe/<int:plan_id>/',views.subscribe_plan),
    path('add_category',views.add_category),
    path('user_products',views.user_product),
    path('product_detail/<int:pk>',views.product_detail),
    path('subscriptionplan',views.subscriptionplan),
    path('addcart/<int:d>',views.addcart),
    path('view_cart/', views.view_cart),
    path('remove_cart/<int:id>', views.remove_cart),
    path('view_wishlist', views.view_wishlist),
    path('add_wishlist/<int:id>', views.add_wishlist),
    path('select_plan/<int:plan_id>/<int:cart_id>', views.select_plan),
    path('payment/<int:d>',views.payment),
    path('my_orders', views.my_orders),
    path('payment_success', views.payment_success),
    path('delivery_dashboard', views.delivery_dashboard),
    path('assign_delivery/<int:booking_id>/<int:delivery_id>/',views.assign_delivery),
    # path('mark_delivered/<int:booking_id>/',views.mark_delivered),
    path('update_delivery/<int:order_id>/<str:action>/', views.update_delivery),
    path('pause_subscription/<int:id>/', views.pause_subscription),
    path('resume_subscription/<int:id>/', views.resume_subscription),
    path('cancel_subscription/<int:id>/', views.cancel_subscription),
    path('admin_bookings', views.admin_bookings),
    path('contact', views.contact),
    path('admin_messages', views.admin_messages),
    path('my_subscription', views.my_subscription),
    path('logout',views.logout),
    path('profile', views.profile),
    path('update_profile', views.update_profile),
    path('update_quantity/<int:cart_id>/<str:action>/', views.update_quantity),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)