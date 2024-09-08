from rest_framework import serializers
from ..models import Item



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'picture', 'category']

    def validate(self, data):
        if data.get('price') <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        if user.role == 'owner':
            restaurant = getattr(user, 'restaurant_profile', None)
        elif user.role == 'employee':
            restaurant = getattr(user.employee_profile, 'restaurant', None)
        else:
            raise serializers.ValidationError("User does not have an associated restaurant.")
        if not restaurant:
            raise serializers.ValidationError("Restaurant associated with the user does not exist.")
 
        validated_data.pop('restaurant', None)

        item = Item.objects.create(restaurant=restaurant, **validated_data)
        return item