import uuid

from django.contrib.auth.models import User
from django.db import transaction
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class GuestSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    visit_time = serializers.DateTimeField(read_only=True)

    @transaction.atomic()
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        random_string = uuid.uuid4()
        username = random_string.hex
        password = str(random_string)
        user_data['username'] = username
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()
        return Guest.objects.create(user=user, **validated_data)

    class Meta:
        model = Guest
        fields = '__all__'


class OrderedPortionSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)

    class Meta:
        model = OrderedPortion
        fields = '__all__'
        read_only_fields = ['order']


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)
    ordered_portions = OrderedPortionSerializer(many=True)

    @transaction.atomic()
    def create(self, validated_data):
        ordered_portions = validated_data.pop('ordered_portions')
        order = Order.objects.create(**validated_data)
        for ordered_portion in ordered_portions:
            ordered_portion['order'] = order
            OrderedPortion.objects.create(**ordered_portion)
        return order

    class Meta:
        model = Order
        fields = '__all__'
