from rest_framework import serializers
from ..models import ModifierGroup


class ModifierGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModifierGroup
        fields = ['id', 'name', 'restaurant']
        read_only_fields = ['restaurant']

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            raise serializers.ValidationError("You are not allowed to create a modifier group.")

        validated_data['restaurant'] = restaurant
        return super().create(validated_data)