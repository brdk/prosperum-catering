from django_filters import rest_framework as filters

from catering.models import Order, Portion


class OrderFilter(filters.FilterSet):
    dish_name = filters.CharFilter(field_name='ordered_portions__portion__name', lookup_expr='iexact')
    restaurant = filters.CharFilter(field_name='restaurant__name')
    date = filters.DateFilter(field_name='date', lookup_expr='date')
    price_min = filters.NumberFilter(method='filter_by_min_price')
    price_max = filters.NumberFilter(method='filter_by_max_price')
    dish_type = filters.CharFilter(method='filter_by_dish_type')

    def filter_by_min_price(self, queryset, name, value):
        order_ids = [order.id for order in queryset if order.total_price >= value]
        return queryset.filter(id__in=order_ids)

    def filter_by_max_price(self, queryset, name, value):
        order_ids = [order.id for order in queryset if order.total_price <= value]
        return queryset.filter(id__in=order_ids)

    def filter_by_dish_type(self, queryset, name, value):
        order_ids = [order.id for order in queryset if order.is_dish_type(value)]
        return queryset.filter(id__in=order_ids)

    class Meta:
        model = Order
        fields = ['restaurant', 'dish_name', 'date', 'price_min', 'price_max', 'dish_type']


class PortionFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='iexact')
    restaurant = filters.CharFilter(field_name='ordered_portions__order__restaurant__name')
    date = filters.DateFilter(field_name='ordered_portions__date', lookup_expr='date')
    price_min = filters.NumberFilter(method='filter_by_min_price')
    price_max = filters.NumberFilter(method='filter_by_max_price')
    dish_type = filters.CharFilter(method='filter_by_dish_type')

    def filter_by_min_price(self, queryset, name, value):
        order_ids = [portion.id for portion in queryset if portion.price >= value]
        return queryset.filter(id__in=order_ids)

    def filter_by_max_price(self, queryset, name, value):
        order_ids = [portion.id for portion in queryset if portion.price <= value]
        return queryset.filter(id__in=order_ids)

    def filter_by_dish_type(self, queryset, name, value):
        order_ids = [portion.id for portion in queryset if portion.cooked_only_with(value)]
        return queryset.filter(id__in=order_ids)

    class Meta:
        model = Portion
        fields = ['restaurant', 'name', 'date', 'price_min', 'price_max', 'dish_type']
