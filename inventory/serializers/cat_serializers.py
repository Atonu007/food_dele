from rest_framework import serializers
from ..models import Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            raise serializers.ValidationError("User does not have an associated restaurant.")
        if not restaurant:
            raise serializers.ValidationError("Restaurant associated with the user does not exist.")

        return Category.objects.create(restaurant=restaurant, **validated_data)
