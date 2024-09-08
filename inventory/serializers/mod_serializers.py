from rest_framework import serializers
from ..models import Modifier,ModifierGroup


class ModifierSerializer(serializers.ModelSerializer):
    modifier_group = serializers.PrimaryKeyRelatedField(queryset=ModifierGroup.objects.all())

    class Meta:
        model = Modifier
        fields = ['id', 'name', 'price', 'restaurant', 'modifier_group']
        read_only_fields = ['restaurant']

    def create(self, validated_data):
        request = self.context.get('request')
        if request.user.role == 'owner':
            restaurant = request.user.restaurant_profile
        elif request.user.role == 'employee':
            restaurant = request.user.employee.restaurant
        else:
            raise serializers.ValidationError("You are not allowed to create a modifier.")
        modifier_group = validated_data.get('modifier_group')
        if modifier_group.restaurant != restaurant:
            raise serializers.ValidationError("Modifier group does not belong to the restaurant.")

        validated_data['restaurant'] = restaurant
        return super().create(validated_data)