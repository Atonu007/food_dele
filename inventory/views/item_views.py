from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsRestaurantOwner, IsEmployee
from ..models import Item
from ..serializers.item_serializers import ItemSerializer



# create an item.
class ItemCreate(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner  | IsEmployee]
    def post(self, request, *args, **kwargs):
        serializer = ItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Retriving the list of item
class ItemList(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner  | IsEmployee]

    def get(self, request, format=None):
        user = request.user
        
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            return Response({"detail": "Not authorized to view items."}, status=status.HTTP_403_FORBIDDEN)
        if not restaurant:
            return Response({"detail": "Restaurant associated with the user does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        items = Item.objects.filter(restaurant=restaurant)
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)


# Item detail, update and delete
class ItemDetail(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner  | IsEmployee]

    def get_object(self, pk, user):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise NotFound("Item not found.")
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            raise PermissionDenied("User does not have access to this item.")
        if not restaurant:
            raise PermissionDenied("Restaurant associated with the user does not exist.")
        if item.restaurant != restaurant:
            raise PermissionDenied("You do not have permission to access this item.")
        
        return item

    def get(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        serializer = ItemSerializer(item, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk, request.user)
        item.delete()
        return Response({"detail": "Item successfully deleted."},status=status.HTTP_204_NO_CONTENT)