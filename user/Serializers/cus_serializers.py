from rest_framework import serializers
from ..models import User,Customer

class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, write_only=True, required=True)
    address = serializers.CharField(required=True)
    contact_number = serializers.CharField(required=True)

    class Meta:
        model = Customer
        fields = ('username', 'password', 'role', 'address', 'contact_number')

    def validate(self, data):
        required_fields = ['username', 'password', 'role', 'address', 'contact_number']
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
        user = User(username=username, role=role, address=address, contact_number=contact_number)
        user.set_password(password)
        user.save()
        Customer.objects.create(user=user)
        
        return user