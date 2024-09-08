from rest_framework import serializers
from ..models import User,Restaurant


# restaurant serializer
class RestaurantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, write_only=True)
    address = serializers.CharField(required=True)
    contact_number = serializers.CharField(required=True)

    class Meta:
        model = Restaurant
        fields = ('name', 'address', 'username', 'password', 'role', 'contact_number')

    def validate(self, data):
        required_fields = ['name', 'username', 'password', 'role', 'address', 'contact_number']
        for field in required_fields:
            if field not in data or not data[field]:
                raise serializers.ValidationError(f'Field needs to be filled: {field}')
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        address = validated_data.pop('address')
        contact_number = validated_data.pop('contact_number')

        user = User(username=username,role=role,address=address,contact_number=contact_number)
        user.set_password(password)
        user.save()
        restaurant = Restaurant.objects.create(owner=user, **validated_data)
        response_data = {
            'name': restaurant.name,
            'address': restaurant.address,
            'contact_number': restaurant.owner.contact_number,
            'role': restaurant.owner.role
        }
        return response_data