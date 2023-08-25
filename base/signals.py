from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import ShippingCost

@receiver(post_migrate)
def create_shipping_cost_row(sender, **kwargs):
    if sender.name == 'base':
        if not ShippingCost.objects.exists():
            ShippingCost.objects.create()