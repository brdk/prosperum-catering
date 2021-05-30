from rest_framework import serializers

from catering.models import City, RestaurantType, Ingredient, Portion, Restaurant, Guest, Order, OrderedPortion


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RestaurantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantType
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class PortionSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()

    class Meta:
        model = Portion
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'


class OrderedPortionSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField()

    class Meta:
        model = OrderedPortion
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField()
    ordered_portions = OrderedPortionSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
