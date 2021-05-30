import enum
import functools

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.functional import cached_property


@enum.unique
class IngredientType(enum.Enum):
    BEEF = 'Beef'
    CHICKEN = 'Chicken'
    PORK = 'Pork'
    VEGETARIAN = 'Vegetarian'
    VEGAN = 'Vegan'

    @staticmethod
    def get_choices():
        return [(t.name, t.value) for t in IngredientType]


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class RestaurantType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=10, choices=IngredientType.get_choices())
    price_per_portion = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Portion(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, default='')
    ingredients = models.ManyToManyField(Ingredient)
    is_beverage = models.BooleanField(default=False)

    @cached_property
    def price(self):
        return sum([ingredient.price_per_portion for ingredient in self.ingredients.all()]) * settings.MARGIN_MULTIPLIER

    def cooked_only_with(self, ingredient_type):
        return all([ingredient.type.lower() == ingredient_type.lower() for ingredient in self.ingredients.all()])

    def __str__(self):
        return self.name


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class Restaurant(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    type = models.ForeignKey(RestaurantType, on_delete=models.PROTECT)
    serves_food = models.BooleanField(default=False)
    serves_beverage = models.BooleanField(default=False)
    menu = models.ManyToManyField(Portion)

    def clean(self):
        super().clean()

        if not self.serves_beverage and self.menu.filter(is_beverage=True).exists():
            raise ValidationError('Restaurant does not serve beverages')

        if not self.serves_food and self.menu.filter(is_beverage=False).exists():
            raise ValidationError('Restaurant does not serve any food')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.clean()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return f'{self.name} in {self.city}'


class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=100)
    visit_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.get_full_name()} visited on {self.visit_time}'


class Order(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.PROTECT, related_name='orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name='guest_orders')
    date = models.DateTimeField(auto_now_add=True)

    @cached_property
    def total_price(self):
        return sum([portion.price for portion in self.ordered_portions.all()])

    @functools.cache
    def is_dish_type(self, dish_type):
        return all([portion.portion.cooked_only_with(dish_type) for portion in self.ordered_portions.all()])

    def __str__(self):
        return f'Order for {self.guest.user.get_full_name()} in {self.restaurant} for {self.total_price}'


class OrderedPortion(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_portions')
    portion = models.ForeignKey(Portion, on_delete=models.CASCADE, related_name='ordered_portions')
    amount = models.PositiveSmallIntegerField()

    @property
    def price(self):
        return self.portion.price * self.amount
