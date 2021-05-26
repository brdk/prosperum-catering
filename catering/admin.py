from django.contrib import admin

from catering.models import City, RestaurantType, Ingredient, Portion, Restaurant, Guest, Order, OrderedPortion


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'price_per_portion', 'total_amount']


class PortionAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_beverage', 'get_ingredients', 'price']

    def get_ingredients(self, obj):
        return ', '.join(obj.ingredients.all().values_list('name', flat=True))
    get_ingredients.short_description = 'ingredients'


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'type', 'serves_food', 'serves_beverage', 'get_menu']

    def get_menu(self, obj):
        return ', '.join(obj.menu.all().values_list('name', flat=True))
    get_menu.short_description = 'menu'


admin.site.register(City)
admin.site.register(RestaurantType)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Portion, PortionAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Guest)
admin.site.register(Order)
admin.site.register(OrderedPortion)
