from django.test import TestCase
from .models import PurchaseOrder
from vendor.models import Vendor
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class PurchaseOrderModelTestCase(TestCase):
    def setUp(self):
        # Initializing test client and user
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        # Creating a test Vendor
        self.vendor = Vendor.objects.create(
            name='Vendor 1',
            contact_details='Contact info 1',
            address='Address 1',
            vendor_code='VC001',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=24.5,
            fulfillment_rate=90.0
        )

        # Creating a test PurchaseOrder
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO0001',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now() + timedelta(days=7),
            items={'item1': 'description1', 'item2': 'description2'},
            quantity=10,
            status='Pending',
            quality_rating=None,
            issue_date=datetime.now(),
            acknowledgement_date=None
        )

    def test_purchase_order_creation(self):
        # Test for PurchaseOrder creation
        purchase_order = PurchaseOrder.objects.get(po_number='PO0000000001')
        self.assertEqual(purchase_order.po_number, 'PO0000000001')
        self.assertEqual(purchase_order.quantity, 10)

    def test_po_number_generation(self):
        # Test the generation of PurchaseOrder number
        new_purchase_order = PurchaseOrder.objects.create(
            vendor=self.vendor,
            delivery_date=datetime.now() + timedelta(days=7),
            items={'item1': 'description1'},
            quantity=5,
            status='Pending'
        )
        self.assertEqual(new_purchase_order.po_number, 'PO0000000002')
