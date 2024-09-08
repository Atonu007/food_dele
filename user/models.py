from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('owner', 'Owner'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    address = models.TextField() 
    contact_number = models.CharField(max_length=11) 

    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users' 

    
    def __str__(self):
        return self.username
    


# restaurant model
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name='restaurant_profile')

    
    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    
    def __str__(self):
        return self.name
    
    
# Employee Model
class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='employee_profile')
    restaurant = models.ForeignKey(Restaurant,related_name='employees',on_delete=models.CASCADE)

    
    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    
    def __str__(self):
        return f'{self.user.username} - {self.restaurant.name}'
    
    
# Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    
    
    def __str__(self):
        return self.user.username