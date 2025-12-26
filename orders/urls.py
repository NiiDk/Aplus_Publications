from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('history/', views.order_history, name='order_history'),
    path('<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('<uuid:order_id>/invoice/', views.order_invoice, name='order_invoice'),
    
    # Payment URLs
    path('payment/initiate/<uuid:order_id>/', views.initialize_payment, name='initiate_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
