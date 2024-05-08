from django.db import models
from vendor.models import Vendor
from django.utils import timezone


# Creating models 
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100,unique=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True, db_constraint=False)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50,default="Pending")
    quality_rating = models.FloatField(null=True,blank=True)
    issue_date = models.DateTimeField(null=True,blank=True)
    acknowledgement_date = models.DateTimeField(null=True,blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)  # New field to record completion date


    def save(self, *args, **kwargs):    
        if not self.pk:
            # Newly created object, so set the creation date
            self.order_date = timezone.now()
            self.issue_date = self.order_date
            self.po_number = self.generate_po_number()

        super().save(*args, **kwargs)    

    #Generate Po number
    def generate_po_number(self):
        #get last po_number
        last_po = PurchaseOrder.objects.order_by('id').last()
        if last_po:
            last_id = last_po.id
            new_id = last_id + 1
        else:
            #if this is the first purchase order
            new_id = 1
        return f"PO{new_id:010d}"

    def __str__(self):
        return f"{self.po_number}"