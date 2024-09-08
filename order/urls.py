from django.urls import path
from .views import CreateOrderView,ListUserOrdersView,CancelOrderView, RestaurantOrdersView, UpdateOrderStatusView

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/', ListUserOrdersView.as_view(), name='user-orders'),
    path('orders/<int:order_id>/cancel/', CancelOrderView.as_view(), name='cancel-order'),

    # restaurant
    path('restaurant-orders/', RestaurantOrdersView.as_view(), name='restaurant-orders'),
    path('orders/<int:order_id>/update-status/', UpdateOrderStatusView.as_view(), name='update-order-status'),
]