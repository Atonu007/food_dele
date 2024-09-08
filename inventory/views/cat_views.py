from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsRestaurantOwner, IsEmployee
from ..models import Category
from ..serializers.cat_serializers import CategorySerializer

# create a new catagorey
class CreateCatagorey(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner  | IsEmployee]

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# catagorey list view
class CategoryList(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner  | IsEmployee]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            return Response({"detail": "User does not have access to categories."}, status=status.HTTP_403_FORBIDDEN)
        if not restaurant:
            return Response({"detail": "Restaurant associated with the user does not exist."}, status=status.HTTP_404_NOT_FOUND)
        categories = Category.objects.filter(restaurant=restaurant)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# Catagorey DetailView, Update And Delete view
class CategoryDetail(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def get_object(self, pk, user):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("Category not found.")
        
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            raise PermissionDenied("User does not have access to this category.")
        
        if not restaurant:
            raise PermissionDenied("Restaurant associated with the user does not exist.")
        
        if category.restaurant != restaurant:
            raise PermissionDenied("You do not have permission to access this category.")
        
        return category

    def get(self, request, pk, *args, **kwargs):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def patch(self, request, pk, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)

    def update(self, request, pk, *args, **kwargs):
        category = self.get_object(pk, request.user)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        category = self.get_object(pk, request.user)
        category.delete()
        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)