from django.contrib import admin
from django.urls import path,include
from app import views

from .views import logout_view

urlpatterns = [

    path('',views.index,name='app'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.index, name='logout'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('products/', views.product_list, name='product_list'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path('album/', views.album_view, name='album'),
    path('add_stamp/', views.add_stamp, name='add_stamp'),
    path('community/', views.community_view, name='community'),
    path('delete_stamp/<int:stamp_id>/', views.delete_stamp, name='delete_stamp'),
    path('edit_stamp/<int:stamp_id>/', views.edit_stamp, name='edit_stamp'),
    path('logout/', logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('place_order/<int:product_id>/', views.place_order, name='place_order'),
    path('interface/', views.payment, name='interface'),

    
  




]