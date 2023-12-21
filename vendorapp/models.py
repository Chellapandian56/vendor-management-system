from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
# from django.contrib.auth.models import User

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
@receiver(pre_save, sender=Vendor)
def generate_vendor_code(sender, instance, **kwargs):
    if not instance.vendor_code:
        instance.vendor_code = get_random_string(length=10).upper()

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} for {self.vendor.name}"
    
@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.delivery_date <= instance.issue_date:
        instance.vendor.on_time_delivery_rate = (
            (instance.vendor.on_time_delivery_rate * instance.vendor.purchaseorder_set.filter(status='completed').count())
            + 1
        ) / (instance.vendor.purchaseorder_set.filter(status='completed').count() + 1)
        instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.quality_rating is not None:
        instance.vendor.quality_rating_avg = (
            (instance.vendor.quality_rating_avg * instance.vendor.purchaseorder_set.filter(status='completed').count())
            + instance.quality_rating
        ) / (instance.vendor.purchaseorder_set.filter(status='completed').count() + 1)
        instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, **kwargs):
    if instance.acknowledgment_date:
        response_time = (instance.acknowledgment_date - instance.issue_date).total_seconds()
        instance.vendor.average_response_time = (
            (instance.vendor.average_response_time * instance.vendor.purchaseorder_set.count())
            + response_time
        ) / (instance.vendor.purchaseorder_set.count() + 1)
        instance.vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.fulfilment_rate = (
            (instance.vendor.fulfilment_rate * instance.vendor.purchaseorder_set.count())
            + 1
        ) / (instance.vendor.purchaseorder_set.count() + 1)
        instance.vendor.save()

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance record for {self.vendor.name} on {self.date}"
