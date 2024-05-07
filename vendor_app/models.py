from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg, F
""""Vendor model to hanle all the vendor activities"""

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

""""Purchase model to handle all the purchase related activity"""

class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )

    
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

""""HistoricalPerformance model for storing the data after calculation of performance matrix"""

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"


@receiver(post_save, sender=PurchaseOrder)
def update_historical_performance(sender, instance, created, **kwargs):
    if created:
        vendor = instance.vendor
        date = instance.order_date.date()

        # Calculate performance metrics
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        print(completed_orders)
        total_completed_orders = completed_orders.count()
        print(total_completed_orders)
        on_time_delivery_rate = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count() / total_completed_orders if total_completed_orders > 0 else 0.0
        print(on_time_delivery_rate)
        quality_rating_avg = completed_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] if total_completed_orders > 0 else 0.0
        average_response_time = completed_orders.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time'] 
        average_response_time = float(average_response_time.total_seconds())
        print(average_response_time,type(average_response_time))
        fulfillment_rate = completed_orders.filter(status='completed').count() / PurchaseOrder.objects.filter(vendor=vendor).count() if PurchaseOrder.objects.filter(vendor=vendor).count() > 0 else 0.0
        print("before updation of the performance matrix")

        # Update HistoricalPerformance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=date)
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.average_response_time = average_response_time
        historical_performance.fulfillment_rate = fulfillment_rate
        historical_performance.save()
    else:
        print('>>>>>>>>>>>>>>>>>')
        # If the PurchaseOrder instance is updated, re-calculate metrics based on all completed orders
        vendor = instance.vendor
        date = instance.order_date.date()

        # Calculate performance metrics
        completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        total_completed_orders = completed_orders.count()
        on_time_delivery_rate = completed_orders.filter(delivery_date__lte=F('acknowledgment_date')).count() / total_completed_orders if total_completed_orders > 0 else 0.0
        quality_rating_avg = completed_orders.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating'] if total_completed_orders > 0 else 0.0
        average_response_time = completed_orders.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))['avg_response_time'] if total_completed_orders > 0 else 0.0
        fulfillment_rate = completed_orders.filter(status='completed').count() / PurchaseOrder.objects.filter(vendor=vendor).count() if PurchaseOrder.objects.filter(vendor=vendor).count() > 0 else 0.0

        # Update HistoricalPerformance record
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=vendor, date=date)
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.average_response_time = average_response_time
        historical_performance.fulfillment_rate = fulfillment_rate
        historical_performance.save()