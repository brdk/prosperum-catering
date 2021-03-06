from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api import filters
from api.serializers import (
    CitySerializer, RestaurantTypeSerializer, IngredientSerializer, PortionSerializer,
    RestaurantSerializer, GuestSerializer, OrderSerializer)
from catering.models import City, RestaurantType, Ingredient, Portion, Restaurant, Guest, Order, OutOfStockError
from catering.tasks import notify_guests


class CityViewSet(ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RestaurantTypeViewSet(ModelViewSet):
    queryset = RestaurantType.objects.all()
    serializer_class = RestaurantTypeSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class PortionViewSet(ModelViewSet):
    queryset = Portion.objects.all()
    serializer_class = PortionSerializer
    filter_class = filters.PortionFilter

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

    @action(detail=True, url_path='guests', methods=['get'])
    def get_guests(self, request, *args, **kwargs):
        guests = Guest.objects.filter(orders__restaurant_id=kwargs['pk'])
        data = GuestSerializer(guests, many=True).data
        return Response(data)

    @action(detail=True, url_path='guests/notify/(?P<date>[0-9-]+)', methods=['get'])
    def notify_guests(self, request, *args, **kwargs):
        notify_guests(kwargs['pk'], kwargs['date'])

        guests = Guest.objects.filter(orders__restaurant__pk=kwargs['pk'],
                                      orders__date__date=kwargs['date'])
        data = GuestSerializer(guests, many=True).data
        return Response(data)

    @action(detail=True, url_path='menu', methods=['get'])
    def get_menu(self, request, *args, **kwargs):
        portions = filters.PortionFilter(data=request.GET, queryset=self.get_object().menu).qs
        data = PortionSerializer(portions, many=True).data
        return Response(data)


class GuestViewSet(ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = filters.OrderFilter

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except OutOfStockError as e:
            return Response({'message': str(e)}, status=400)

    @action(detail=False, url_path='total', methods=['get'])
    def total_orders(self, request, *args, **kwargs):
        orders = self.filter_queryset(self.queryset)
        data = {
            'total': orders.count()
        }
        return Response(data)
