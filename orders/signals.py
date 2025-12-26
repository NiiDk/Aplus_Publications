from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, QuoteRequest
from .services import NotificationService

@receiver(post_save, sender=Order)
def handle_order_notifications(sender, instance, created, **kwargs):
    if created:
        NotificationService.alert_admin_new_order(instance)
    else:
        NotificationService.notify_order_status_change(instance)

@receiver(post_save, sender=QuoteRequest)
def handle_quote_notifications(sender, instance, created, **kwargs):
    if created:
        NotificationService.alert_admin_new_quote(instance)
    else:
        NotificationService.notify_quote_status_change(instance)
