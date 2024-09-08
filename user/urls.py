from django.urls import path
from .view.res_views import RestaurantSignUp
from .view.emp_views import EmployeeSignUp
from .view.cus_views import CustomerSignUp
from .view.login_views import Login

urlpatterns = [
    path('restaurant/signup/', RestaurantSignUp.as_view(), name='register-restaurant'),
    path('employee/signup/', EmployeeSignUp.as_view(), name='register-employee'),
    path('customer/signup/', CustomerSignUp.as_view(), name='register-customer'),

    path('login/', Login.as_view(), name='login'),
    
   
]