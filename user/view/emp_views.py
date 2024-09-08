from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsRestaurantOwner
from ..models import Restaurant,Employee
from ..Serializers.emp_serializers import EmployeeSerializer,EmployeeListSerializer,EmployeeDetailSerializer


class EmployeeSignUp(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class EmployeeList(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner]

    def get(self, request, format=None):
        try:
            restaurant = request.user.restaurant_profile
        except Restaurant.DoesNotExist:
            return Response({'detail': 'No restaurant associated with this user.'}, status=status.HTTP_404_NOT_FOUND)

        employees = Employee.objects.filter(restaurant=restaurant)
        serializer = EmployeeListSerializer(employees, many=True)
        
        response_data = {
            'employee_count': employees.count(),
            'employees': serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)



class EmployeeDetail(APIView):
    permission_classes = [IsAuthenticated, IsRestaurantOwner]
    def get(self, request, pk, format=None):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeDetailSerializer(employee)
        return Response(serializer.data)