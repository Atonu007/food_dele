from rest_framework import serializers
from inventory.models import Modifier,Item
from user.models import User
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    modifiers = serializers.PrimaryKeyRelatedField(queryset=Modifier.objects.all(), many=True, required=False)
    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())

    class Meta:
        model = OrderItem
        fields = ['id', 'item', 'quantity', 'modifiers']




class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'address', 'total_price', 'created_at', 'updated_at', 'status', 'payment_method', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        if not items_data:
            raise serializers.ValidationError("At least one item is required to create an order.")
        first_item_data = items_data[0]
        item_instance = first_item_data.get('item')
        
        if not isinstance(item_instance, Item):
            raise serializers.ValidationError("Item must be a valid Item instance.")
        
        restaurant = item_instance.restaurant
        customer = validated_data.get('customer')
        
        if isinstance(customer, User):
            customer_id = customer.id
        else:
            customer_id = customer
        
        try:
            user = User.objects.get(id=customer_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with the given ID does not exist.")
        address = user.address  
        order = Order.objects.create(
            **validated_data,
            restaurant=restaurant,
            address=address
        )
        
        for item_data in items_data:
            modifiers_data = item_data.pop('modifiers', [])
            item_instance = item_data.get('item')
            
            if not isinstance(item_instance, Item):
                raise serializers.ValidationError("Item must be a valid Item instance.")
            
            order_item = OrderItem.objects.create(
                order=order,
                item=item_instance,
                quantity=item_data.get('quantity', 1)
            )
            order_item.modifiers.set(modifiers_data)
        
        order.calculate_total_price()
        return order



