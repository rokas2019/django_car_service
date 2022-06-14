from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registered_cars/', views.registered_cars, name='registered_cars'),
    path('registered_cars/<int:registered_car_id>', views.registered_car, name='registered_car'),
    path('car_models/', views.car_models, name='car_models'),
    path('car_models/<int:car_model_id>', views.car_model, name='car_model'),
    path('orders/', views.OrdersListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('myorders/', views.ServiceOrdersByUserListView.as_view(), name='my-orders'),
]
