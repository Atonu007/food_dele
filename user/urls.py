from django.urls import path
from .view.res_views import RestaurantSignUp,RestaurantList,RestaurantDetail
from .view.emp_views import EmployeeSignUp,EmployeeList,EmployeeDetail
from .view.cus_views import CustomerSignUp
from .view.login_views import Login

urlpatterns = [
    path('restaurant/signup/', RestaurantSignUp.as_view(), name='register-restaurant'),
    path('employee/signup/', EmployeeSignUp.as_view(), name='register-employee'),
    path('customer/signup/', CustomerSignUp.as_view(), name='register-customer'),

    path('login/', Login.as_view(), name='login'),


    # for user viewing restaurant
    path('restaurants/', RestaurantList.as_view(), name='restaurant-list'),
    path('restaurants/<int:pk>/', RestaurantDetail.as_view(), name='restaurant-detail'),


     # for restaurant owner
    path('employees/', EmployeeList.as_view(), name='employee-list'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee-detail'),
    
   
]