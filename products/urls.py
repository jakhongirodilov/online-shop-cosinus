from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    
    path('product/<int:id>/', views.product, name="product"),
    path('new_product/', views.new_product, name='new_product'),
    path('edit_product/<int:pk>/', views.edit_product, name="edit_product"),
    path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
    
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('reduce_quantity/<int:pk>', views.reduce_quantity, name='reduce_quantity'),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove_from_cart"),

    path('place_order/', views.place_order, name='place_order'),
    path('checkout', views.create_stripe_checkout_session, name="checkout"),
    path('success/', views.success, name="success"),
    path('cancel/', views.fail, name="fail"),
    path('orders/', views.orders, name='orders'),
    path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
]
