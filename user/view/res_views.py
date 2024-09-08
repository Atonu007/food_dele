from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsCustomer
from ..pagination import Pagination
from ..Serializers.res_serializers import RestaurantSerializer, RestaurantDetailSerializer
from ..models import Restaurant

class RestaurantSignUp(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# view all restaurant
class RestaurantList(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request):
        restaurants = Restaurant.objects.all()
        paginator = Pagination()
        paginated_restaurants = paginator.paginate_queryset(restaurants, request)
        data = []
        for restaurant in paginated_restaurants:
            owner = restaurant.owner
            data.append({
                'name': restaurant.name,
                'address': restaurant.address,
                'username': owner.username,
                'password': '',  
                'role': owner.role,
                'contact_number': owner.contact_number,
            })
        serializer = RestaurantSerializer(data, many=True)
        return paginator.get_paginated_response(serializer.data)


    
# view detail restaurant
class RestaurantDetail(APIView):
    def get(self, request, *args, **kwargs):
        try:
            restaurant_id = kwargs.get('pk')
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data, status=status.HTTP_200_OK)