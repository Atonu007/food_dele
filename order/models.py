from django.db import models
from user.models import Restaurant,User
from inventory.models import Item, Modifier



class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('canceled', 'Canceled'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('cash', 'Cash'),
        ('card', 'Card'),
    )
    restaurant = models.ForeignKey(Restaurant, related_name='orders', on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, default='demo')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
  
    def calculate_total_price(self):
        total = 0
        for item in self.items.all():
            item_total = item.item.price * item.quantity
            for modifier in item.modifiers.all():
                item_total += modifier.price
            total += item_total
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id} by {self.customer.username} at {self.restaurant.name}"
    



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    modifiers = models.ManyToManyField(Modifier, related_name='order_items', blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.item.name}"
    


class Payment(models.Model):
    order = models.OneToOneField('Order', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"