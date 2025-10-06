from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceItem, Transaction

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Get JWT token
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
    
    def test_create_invoice(self):
        """Test invoice creation with items"""
        data = {
            'customer_name': 'Test Customer',
            'items': [
                {'description': 'Item 1', 'quantity': 2, 'unit_price': '10.00'},
                {'description': 'Item 2', 'quantity': 1, 'unit_price': '20.00'}
            ]
        }
        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceItem.objects.count(), 2)
        
        invoice = Invoice.objects.first()
        self.assertEqual(float(invoice.total_amount), 40.00)
        self.assertEqual(Transaction.objects.filter(transaction_type='Sale').count(), 1)
    
    def test_create_invoice_without_items(self):
        """Test that invoice without items fails"""
        data = {
            'customer_name': 'Test Customer',
            'items': []
        }
        response = self.client.post('/api/invoices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_pay_invoice(self):
        """Test marking invoice as paid"""
        # Create invoice first
        invoice = Invoice.objects.create(customer_name='Test Customer')
        InvoiceItem.objects.create(invoice=invoice, description='Item', quantity=1, unit_price=100)
        invoice.update_total_amount()
        
        # Pay the invoice
        response = self.client.post(f'/api/invoices/{invoice.id}/pay/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'Paid')
        self.assertEqual(Transaction.objects.filter(transaction_type='Payment').count(), 1)
    
    def test_cannot_pay_already_paid_invoice(self):
        """Test that paid invoice cannot be paid again"""
        invoice = Invoice.objects.create(customer_name='Test Customer', status='Paid')
        InvoiceItem.objects.create(invoice=invoice, description='Item', quantity=1, unit_price=100)
        
        response = self.client.post(f'/api/invoices/{invoice.id}/pay/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
