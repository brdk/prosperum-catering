from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import filters
from api.serializers import (
    CitySerializer, RestaurantTypeSerializer, IngredientSerializer, PortionSerializer,
    RestaurantSerializer, GuestSerializer, OrderSerializer)
from catering.models import City, RestaurantType, Ingredient, Portion, Restaurant, Guest, Order


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAdminUser]


class RestaurantTypeViewSet(ModelViewSet):
    queryset = RestaurantType.objects.all()
    serializer_class = RestaurantTypeSerializer
    permission_classes = [IsAdminUser]


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminUser]


class PortionViewSet(ModelViewSet):
    queryset = Portion.objects.all()
    serializer_class = PortionSerializer
    permission_classes = [IsAdminUser]


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]


class GuestViewSet(ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAdminUser]


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.OrderFilter
    permission_classes = [IsAdminUser]

    @action(detail=False, url_path='total', methods=['get'])
    def total_orders(self, request, *args, **kwargs):
        orders = self.filter_queryset(self.queryset)
        data = {
            'total': orders.count()
        }
        return Response(data)
