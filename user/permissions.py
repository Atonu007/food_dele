from rest_framework.permissions import BasePermission

class IsRestaurantOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'owner'

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'customer'

class IsRestaurantOwnerOrEmployee(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user and (user.role == 'owner' or user.role == 'employee')