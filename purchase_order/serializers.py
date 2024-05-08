from rest_framework import serializers
from .models import PurchaseOrder



class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    # Validates the quantity field
    def validate_quantity(self,value):
        if value <= 0:
            raise serializers.ValidationError('Quantity Cannot be less than 1')
        return value

    # Validates the status field
    def validate_status(self,value):
        current_status = self.instance.status

        if current_status and current_status.lower() != 'pending': #
            raise serializers.ValidationError('Status cannot be changed')
        
        if value.lower() not in ['completed','cancelled']:
            raise serializers.ValidationError('Please Enter Valid Status')
        
        return value.lower()

    # Validates the quality_rating field
    def validate_quality_rating(self,value):
        current_status = self.instance.status
        if current_status.lower() != 'completed':
            raise serializers.ValidationError('Cannot give Quality rating ')
        if value not in range(1,11):
            raise serializers.ValidationError('Quality Rating must between 1-10')
        
        return value
        
            

