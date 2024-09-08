from rest_framework import serializers
from ..models import User



# User serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    address = serializers.CharField(required=True)
    contact_number = serializers.CharField(required=True)

    
    class Meta:
        model = User
        fields = ('username', 'password', 'role', 'address', 'contact_number')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role'],
            address=validated_data.get('address', ''),
            contact_number=validated_data.get('contact_number', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user