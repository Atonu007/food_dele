from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .sslecommerce import ssl
from .serializers import OrderSerializer
from .models import Order,Payment
from user.permissions import IsCustomer,IsRestaurantOwnerOrEmployee
from .function import generate_transaction_id




class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        gateway_page_url = ''
        if not hasattr(user, 'customer_profile'):
            return Response({"detail": "You must be a customer to create an order."}, status=status.HTTP_403_FORBIDDEN)
        request.data['customer'] = user.id
       
       
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():

            order = serializer.save()
            response_data = OrderSerializer(order).data
            
            transaction_id = generate_transaction_id()
            
            if response_data['payment_method'] == "card":
                response = ssl(transaction_id,response_data['total_price'])
                
                gateway_page_url = response.get('GatewayPageURL')
               
            payment = Payment.objects.create(
                order=order,
                total_price=response_data['total_price'],
                transaction_id=transaction_id,  
                
            )
            response_data['gateway_page_url'] = gateway_page_url

            return Response(response_data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ListUserOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def get(self, request, *args, **kwargs):
        user = request.user
        if not hasattr(user, 'customer_profile'):
            return Response({"detail": "You must be a customer to view orders."}, status=status.HTTP_403_FORBIDDEN)
        orders = Order.objects.filter(customer=user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = kwargs.get('order_id')
        if not hasattr(user, 'customer_profile'):
            return Response({"detail": "You must be a customer to cancel an order."}, status=status.HTTP_403_FORBIDDEN)
        try:
            order = Order.objects.get(id=order_id, customer=user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found or you do not have permission to cancel this order."}, status=status.HTTP_404_NOT_FOUND)

        if order.status != "pending":
            return Response({"detail": "Only orders in the 'processing' state can be canceled."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = "canceled"
        order.save()

        return Response({"detail": "Order has been canceled successfully."}, status=status.HTTP_200_OK)



class RestaurantOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwnerOrEmployee]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.role == 'owner':
            try:
                restaurant = user.restaurant_profile
            except AttributeError:
                return Response({"detail": "Restaurant profile not found for the owner."}, status=status.HTTP_404_NOT_FOUND)
        elif user.role == 'employee':
            try:
                restaurant = user.employee_profile.restaurant
            except AttributeError:
                return Response({"detail": "Restaurant profile not found for the employee."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "User does not have a valid role to access orders."}, status=status.HTTP_403_FORBIDDEN)
        orders = Order.objects.filter(restaurant=restaurant)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwnerOrEmployee]

    def patch(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        new_status = request.data.get('status')
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            return Response({"detail": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        user = request.user
        if user.role == 'owner':
            if order.restaurant != user.restaurant_profile:
                return Response({"detail": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
        elif user.role == 'employee':
            if order.restaurant != user.employee_profile.restaurant:
                return Response({"detail": "You do not have permission to update this order."}, status=status.HTTP_403_FORBIDDEN)
        if order.status == 'canceled':
            return Response({"detail": "Cannot change the status of a canceled order."}, status=status.HTTP_400_BAD_REQUEST)

        if order.status == 'pending' and new_status in ['canceled', 'processed']:
            order.status = new_status
            order.save()
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        if order.status == 'processed' and new_status == 'canceled':
            return Response({"detail": "Cannot change the status from processed to canceled."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Invalid status transition."}, status=status.HTTP_400_BAD_REQUEST)