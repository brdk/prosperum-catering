from celery import shared_task

from catering.models import Guest, Restaurant
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
