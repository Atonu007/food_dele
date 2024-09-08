from rest_framework import serializers
from ..models import User,Restaurant,Employee

class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, write_only=True)
    address = serializers.CharField(write_only=True)
    contact_number = serializers.CharField(write_only=True)
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)

    class Meta:
        model = Employee
        fields = ('username', 'password', 'role', 'address', 'contact_number', 'restaurant', 'restaurant_name')

    def validate(self, data):
        required_fields = ['username', 'password', 'role', 'address', 'contact_number', 'restaurant']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError({field: f'Field needs to be filled: {field}'})
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        address = validated_data.pop('address')
        contact_number = validated_data.pop('contact_number')
        restaurant = validated_data.pop('restaurant')
        user = User.objects.create(username=username,role=role,address=address,contact_number=contact_number,)
        user.set_password(password)
        user.save()
        employee = Employee.objects.create(user=user,restaurant=restaurant)

        return employee