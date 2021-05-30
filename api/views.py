from django.db.models import Sum
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
from catering.tasks import notify_guests


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
    filter_class = filters.PortionFilter
    permission_classes = [IsAdminUser]

    @action(detail=False, url_path='top(/(?P<limit>[0-9]+))?', methods=['get'])
    def total_orders(self, request, *args, **kwargs):
        limit = kwargs.get('limit')
        portions = self.filter_queryset(self.queryset)
        portions = portions.annotate(ordered_times=Sum('ordered_portions__amount')).order_by('-ordered_times')
        if limit:
            limit = int(limit)
            portions = portions[:limit]
        data = self.serializer_class(portions, many=True).data
        return Response(data)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, url_path='guests', methods=['get'])
    def get_guests(self, request, *args, **kwargs):
        guests = Guest.objects.filter(user__orders__restaurant_id=kwargs['pk'])
        data = GuestSerializer(guests, many=True).data
        return Response(data)

    @action(detail=True, url_path='guests/notify/(?P<date>[0-9-]+)', methods=['get'])
    def notify_guests(self, request, *args, **kwargs):
        notify_guests(kwargs['pk'], kwargs['date'])

        guests = Guest.objects.filter(user__orders__restaurant__pk=kwargs['pk'],
                                      user__orders__date__date=kwargs['date'])
        data = GuestSerializer(guests, many=True).data
        return Response(data)


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
