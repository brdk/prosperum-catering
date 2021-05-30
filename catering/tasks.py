from celery import shared_task

from catering.models import Guest, Restaurant, Ingredient
from catering.tools import send_fake_email


def notify_guests(restaurant_id, date):
    for guest_id in (Guest.objects.filter(orders__restaurant_id=restaurant_id,
                                          orders__date__date=date)
                                  .values_list('id', flat=True)):
        notify_guest.delay(guest_id, restaurant_id, date)


@shared_task
def notify_guest(guest_id, restaurant_id, date):
    guest = Guest.objects.prefetch_related('user').get(id=guest_id)
    restaurant = Restaurant.objects.get(id=restaurant_id)
    message = f'Dear {guest.user.get_full_name()}, you visited restaurant {restaurant.name} on {date}'
    send_fake_email(guest.user.email, message)


@shared_task
def notify_owner(restaurant_id, ingredient_ids):
    restaurant = Restaurant.objects.select_related('owner__user').get(id=restaurant_id)
    owner_user = restaurant.owner.user
    ingredients = ', '.join(
        Ingredient.objects.filter(id__in=ingredient_ids).values_list('name', flat=True)
    )
    message = f'Dear {owner_user.get_full_name()}, ingredients {ingredients} are out of stock'
    send_fake_email(owner_user.email, message)
