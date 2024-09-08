from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsRestaurantOwner, IsEmployee
from ..models import ModifierGroup
from ..serializers.modGroup_serializers import ModifierGroupSerializer


# create Modifier Group.
class GroupModifierCreate(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def post(self, request, *args, **kwargs):
        serializer = ModifierGroupSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ModifierGroupList(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def get(self, request, *args, **kwargs):
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to view modifier groups."}, status=status.HTTP_403_FORBIDDEN)
        modifier_groups = ModifierGroup.objects.filter(restaurant=restaurant)
        serializer = ModifierGroupSerializer(modifier_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ModifierGroupDetail(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def get_object(self, pk):
        try:
            return ModifierGroup.objects.get(pk=pk)
        except ModifierGroup.DoesNotExist:
            raise NotFound("Category not found.")

    def get(self, request, pk, *args, **kwargs):
        modifier_group = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to view this modifier group."}, status=status.HTTP_403_FORBIDDEN)
        if modifier_group.restaurant != restaurant:
            return Response({"detail": "Modifier group does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ModifierGroupSerializer(modifier_group)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        modifier_group = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to update this modifier group."}, status=status.HTTP_403_FORBIDDEN)
        
        if modifier_group.restaurant != restaurant:
            return Response({"detail": "Modifier group does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ModifierGroupSerializer(modifier_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        modifier_group = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to delete this modifier group."}, status=status.HTTP_403_FORBIDDEN)
        
        if modifier_group.restaurant != restaurant:
            return Response({"detail": "Modifier group does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        
        modifier_group.delete()
        return Response({"detail": "Item successfully deleted."},status=status.HTTP_204_NO_CONTENT)