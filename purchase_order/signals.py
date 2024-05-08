from django.db.models import *
from purchase_order.models import PurchaseOrder
from vendor_historical_performance.models import HistoricalPerformance
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


# Update the average response time of a vendor based on acknowledgment date
@receiver(post_save,sender=PurchaseOrder)
def update_response_time(sender,instance,created,**kwargs):
    if instance.acknowledgement_date is not None:
        vendor = instance.vendor
        all_pos = PurchaseOrder.objects.filter(vendor=vendor)
        ack_pos = all_pos.filter(acknowledgement_date__isnull=False)
        ack_pos = ack_pos.annotate(response=ExpressionWrapper(
            F('acknowledgement_date')-F('issue_date'),
            output_field=DurationField()
            ))
        sum_response = ack_pos.aggregate(Sum('response'))
        days = sum_response['response__sum'].total_seconds()/(60*60*24)
        avg_response = days/len(all_pos)
        vendor.average_response_time = round(avg_response,1)
        print(avg_response)
        vendor.save()
        
# Update the on-time delivery rate of a vendor
@receiver(post_save,sender=PurchaseOrder)
def update_complete_delivery(sender,instance,created,**kwargs):
    if instance.status == 'Completed' and instance.completion_date is None:
        instance.completion_date = timezone.now()
        instance.save()

        #calculating on_time_delivery_rate
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor,status='Completed')
        on_time_delivery_pos = completed_pos.filter(
            completion_date__lte=instance.delivery_date
            ).count()
        vendor.on_time_delivery_rate =(on_time_delivery_pos/len(completed_pos))*100
        vendor.save()

# Update the average quality rating of a vendor
@receiver(post_save,sender=PurchaseOrder)
def quality_rating_average(sender,instance,created,**kwargs):
    if instance.status == "Completed" and instance.quality_rating is not None:
        vendor = instance.vendor
        vendor_pos = PurchaseOrder.objects.filter(vendor=vendor)
        completed_pos = vendor_pos.filter(status='Completed')
        vendor.quality_rating_avg = completed_pos.aggregate(avg_rating=Avg('quality_rating'))['avg_rating'] or vendor.quality_rating_avg
        vendor.save(update_fields=['quality_rating_avg'])

# Update the fulfillment rate of a vendor
@receiver(post_save,sender=PurchaseOrder)
def fulfillment_rate(sender,instance,created,**kwargs):
    if instance.status in ['Completed', 'Cancelled']:
        vendor = instance.vendor
        vendor_pos = PurchaseOrder.objects.filter(vendor=vendor)
        try:
            if vendor_pos.exists():
                success_pos = vendor_pos.filter(status='Completed',completion_date__lte=instance.delivery_date)
                fulfillment_rate = (success_pos.count()/vendor_pos.count())*100
        except ZeroDivisionError:
            print('Division by zero error occured')
        except Exception as e:
            print(e)

        vendor.fulfillment_rate = round(fulfillment_rate,2) if fulfillment_rate is not None else vendor.fulfillment_rate
        vendor.save(update_fields=['fulfillment_rate'])

# Add performance metrics to the HistoricalPerformance model
@receiver(post_save,sender=PurchaseOrder)
def add_performance_metrics(sender,instance,created,**kwargs):
    if not created:
        try:
            vendor = instance.vendor
            print("vendor is...",vendor)
            if not instance._state.adding:
                #creating new entry in historical performance
                HistoricalPerformance.objects.create(
                    vendor = vendor,
                    date = timezone.now(),
                    on_time_delivery_rate = vendor.on_time_delivery_rate,
                    quality_rating_avg = vendor.quality_rating_avg,
                    average_response_time = vendor.average_response_time,
                    fulfillment_rate = vendor.fulfillment_rate
                )

        except Exception as e:
            print("unable to add data to Historical performance...",e)


        

