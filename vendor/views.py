from rest_framework import viewsets
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class VendorViewSet(viewsets.ModelViewSet):
    # Define initial queryset
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True,methods=['get'])
    def performance(self,request,pk=None): 
        # Retrieve the vendor object
        vendor = self.get_object()

        # Prepare and return performance metrics as a response
        performance_metrics = {
            'vendor_name': vendor.name,
            'on_time_delivery_rate':vendor.on_time_delivery_rate,
            'quality_rating_avg':vendor.quality_rating_avg,
            'average_response_time':vendor.average_response_time,
            'fulfillment_rate':vendor.fulfillment_rate
        }
        return Response(performance_metrics)
