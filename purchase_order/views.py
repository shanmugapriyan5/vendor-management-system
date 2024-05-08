from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import PurchaseOrder
from vendor.models import Vendor
from .serializers import  PurchaseOrderSerializer
from django.utils import timezone


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    # Query all PurchaseOrder instances
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer



    @action(detail=True,methods=['post'])
    def acknowledge(self,request,pk=None):
        """
        Acknowledge a PurchaseOrder by updating its 'acknowledgement_date'.

        Args:
        - request: HTTP request object.
        - pk (int): Primary key of the PurchaseOrder instance.

        Returns:
        - Response: Detailed information of the acknowledged PurchaseOrder.
        """
        purchaseorder = self.get_object()

        # Check if the 'acknowledgement_date' is not set
        if not purchaseorder.acknowledgement_date:
            try:
                # Set 'acknowledgement_date' to current timestamp
                purchaseorder.acknowledgement_date = timezone.now()
                purchaseorder.save()
            except Exception as e:
                print(e)

        # Construct detailed information of the acknowledged PurchaseOrder
        purchaseorder_detail = {
            'purchase_order':purchaseorder.po_number,
            'vendor':purchaseorder.vendor.name,
            'order_date':purchaseorder.order_date,
            'delivery_date':purchaseorder.delivery_date,
            'items':purchaseorder.items,
            'quantity':purchaseorder.quantity,
            'status':purchaseorder.status,
            'quality_rating':purchaseorder.quality_rating,
            'issue_date':purchaseorder.issue_date,
            'acknowledgement_date':purchaseorder.acknowledgement_date
        }

        return Response(purchaseorder_detail)

