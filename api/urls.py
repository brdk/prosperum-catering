from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter(trailing_slash=True)
router.register('cities', views.CityViewSet)
router.register('restaurant-types', views.RestaurantTypeViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('portions', views.PortionViewSet)
router.register('restaurants', views.RestaurantViewSet)
router.register('guests', views.GuestViewSet)
router.register('orders', views.OrderViewSet)
urlpatterns = router.urls
