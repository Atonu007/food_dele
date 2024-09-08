from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from user.permissions import IsRestaurantOwner, IsEmployee
from ..models import Modifier
from ..serializers.mod_serializers import ModifierSerializer


# Create Modifier.
class ModifierCreate(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def post(self, request, *args, **kwargs):
        serializer = ModifierSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# list of all modifier
class ModifierList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.role == 'owner':
            restaurant = user.restaurant_profile
        elif user.role == 'employee':
            restaurant = user.employee.restaurant
        else:
            return Response({"detail": "You are not allowed to view modifiers."}, status=status.HTTP_403_FORBIDDEN)

        modifiers = Modifier.objects.filter(restaurant=restaurant)
        serializer = ModifierSerializer(modifiers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# Modifier detail and update and delete
class ModifierDetail(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner | IsEmployee]

    def get_object(self, pk):
        try:
            return Modifier.objects.get(pk=pk)
        except Modifier.DoesNotExist:
            raise NotFound("Modifier not found.")

    def get(self, request, pk, *args, **kwargs):
        modifier = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to view this modifier."}, status=status.HTTP_403_FORBIDDEN)
        
        if modifier.restaurant != restaurant:
            return Response({"detail": "Modifier does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ModifierSerializer(modifier)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        modifier = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to update this modifier."}, status=status.HTTP_403_FORBIDDEN)
        
        if modifier.restaurant != restaurant:
            return Response({"detail": "Modifier does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ModifierSerializer(modifier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        modifier = self.get_object(pk)
        
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            return Response({"detail": "You do not have permission to delete this modifier."}, status=status.HTTP_403_FORBIDDEN)
        if modifier.restaurant != restaurant:
            return Response({"detail": "Modifier does not belong to your restaurant."}, status=status.HTTP_403_FORBIDDEN)
        modifier.delete()
        return Response({"detail": "Modifier successfully deleted."}, status=status.HTTP_204_NO_CONTENT)