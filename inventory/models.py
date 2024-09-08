from django.db import models
from user.models import Restaurant

#Category models.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    restaurant = models.ForeignKey(Restaurant,related_name='categories',on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

# Item model.
class Item(models.Model):
    category = models.ForeignKey(Category,related_name='items',on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='item_pictures/')
    restaurant = models.ForeignKey(Restaurant, related_name='items', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return f'{self.name} - {self.restaurant.name}'
    

# ModifierGroup Model.
class ModifierGroup(models.Model):
    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(Restaurant,related_name='modifier_groups', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Modifier Group'
        verbose_name_plural = 'Modifier Groups'
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return f'{self.name} - {self.restaurant.name}'


class Modifier(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, related_name='modifiers', on_delete=models.CASCADE)
    modifier_group = models.ForeignKey(ModifierGroup, related_name='modifiers', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Modifier'
        verbose_name_plural = 'Modifiers'
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return f'{self.name} - {self.restaurant.name}'
