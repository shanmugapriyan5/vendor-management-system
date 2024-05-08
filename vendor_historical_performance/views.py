from rest_framework import viewsets
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer



class HistorialPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistoricalPerformanceSerializer

    def get_queryset(self):
        # Retrieve the vendor_id from URL kwargs
        vendor_id = self.kwargs.get('vendor_id')

        # Filter queryset based on vendor_id or return all HistoricalPerformance objects
        if vendor_id is not None:
            queryset = HistoricalPerformance.objects.filter(vendor=vendor_id)
        else:
            queryset = HistoricalPerformance.objects.all()
            
        return queryset