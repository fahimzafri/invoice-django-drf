from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Invoice, InvoiceItem, Transaction
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Invoice.objects.all().delete()
        Transaction.objects.all().delete()
        
        # Create test users if they don't exist
        self.stdout.write('Creating users...')
        if not User.objects.filter(username='zafri').exists():
            User.objects.create_user(username='zafri', password='zafri', email='zafri@example.com')
            self.stdout.write(self.style.SUCCESS('Created user: zafri'))
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(username='admin', password='admin123', email='admin@example.com')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin'))

        # Create sample invoices
        self.stdout.write('Creating sample invoices...')
        
        # Invoice 1 - Pending
        invoice1 = Invoice.objects.create(
            customer_name='Acme Corporation',
            status='Pending'
        )
        InvoiceItem.objects.create(
            invoice=invoice1,
            description='Website Development',
            quantity=1,
            unit_price=Decimal('5000.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice1,
            description='SEO Optimization',
            quantity=1,
            unit_price=Decimal('1500.00')
        )
        invoice1.update_total_amount()
        Transaction.objects.create(
            invoice=invoice1,
            transaction_type='Sale',
            amount=invoice1.total_amount
        )
        self.stdout.write(self.style.SUCCESS(f'Created Invoice: {invoice1.reference_number} - ${invoice1.total_amount}'))

        # Invoice 2 - Paid
        invoice2 = Invoice.objects.create(
            customer_name='Tech Solutions Ltd',
            status='Pending'
        )
        InvoiceItem.objects.create(
            invoice=invoice2,
            description='Mobile App Development',
            quantity=1,
            unit_price=Decimal('8000.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice2,
            description='UI/UX Design',
            quantity=1,
            unit_price=Decimal('2000.00')
        )
        invoice2.update_total_amount()
        Transaction.objects.create(
            invoice=invoice2,
            transaction_type='Sale',
            amount=invoice2.total_amount
        )
        # Mark as paid
        invoice2.status = 'Paid'
        invoice2.save()
        Transaction.objects.create(
            invoice=invoice2,
            transaction_type='Payment',
            amount=invoice2.total_amount
        )
        self.stdout.write(self.style.SUCCESS(f'Created Invoice: {invoice2.reference_number} - ${invoice2.total_amount} (PAID)'))

        # Invoice 3 - Pending
        invoice3 = Invoice.objects.create(
            customer_name='Global Enterprises',
            status='Pending'
        )
        InvoiceItem.objects.create(
            invoice=invoice3,
            description='Cloud Infrastructure Setup',
            quantity=3,
            unit_price=Decimal('1200.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice3,
            description='Security Audit',
            quantity=1,
            unit_price=Decimal('3000.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice3,
            description='Technical Support (Monthly)',
            quantity=6,
            unit_price=Decimal('500.00')
        )
        invoice3.update_total_amount()
        Transaction.objects.create(
            invoice=invoice3,
            transaction_type='Sale',
            amount=invoice3.total_amount
        )
        self.stdout.write(self.style.SUCCESS(f'Created Invoice: {invoice3.reference_number} - ${invoice3.total_amount}'))

        # Invoice 4 - Paid
        invoice4 = Invoice.objects.create(
            customer_name='Startup Inc',
            status='Pending'
        )
        InvoiceItem.objects.create(
            invoice=invoice4,
            description='Logo Design',
            quantity=1,
            unit_price=Decimal('800.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice4,
            description='Brand Guidelines',
            quantity=1,
            unit_price=Decimal('1200.00')
        )
        invoice4.update_total_amount()
        Transaction.objects.create(
            invoice=invoice4,
            transaction_type='Sale',
            amount=invoice4.total_amount
        )
        # Mark as paid
        invoice4.status = 'Paid'
        invoice4.save()
        Transaction.objects.create(
            invoice=invoice4,
            transaction_type='Payment',
            amount=invoice4.total_amount
        )
        self.stdout.write(self.style.SUCCESS(f'Created Invoice: {invoice4.reference_number} - ${invoice4.total_amount} (PAID)'))

        # Invoice 5 - Pending (Large order)
        invoice5 = Invoice.objects.create(
            customer_name='Enterprise Solutions Co',
            status='Pending'
        )
        InvoiceItem.objects.create(
            invoice=invoice5,
            description='ERP System Development',
            quantity=1,
            unit_price=Decimal('25000.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice5,
            description='Data Migration',
            quantity=1,
            unit_price=Decimal('5000.00')
        )
        InvoiceItem.objects.create(
            invoice=invoice5,
            description='Training Sessions',
            quantity=10,
            unit_price=Decimal('500.00')
        )
        invoice5.update_total_amount()
        Transaction.objects.create(
            invoice=invoice5,
            transaction_type='Sale',
            amount=invoice5.total_amount
        )
        self.stdout.write(self.style.SUCCESS(f'Created Invoice: {invoice5.reference_number} - ${invoice5.total_amount}'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== SEED DATA SUMMARY ==='))
        self.stdout.write(self.style.SUCCESS(f'Total Invoices: {Invoice.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Pending Invoices: {Invoice.objects.filter(status="Pending").count()}'))
        self.stdout.write(self.style.SUCCESS(f'Paid Invoices: {Invoice.objects.filter(status="Paid").count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Transactions: {Transaction.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'\nTest Credentials:'))
        self.stdout.write(self.style.SUCCESS('Username: zafri | Password: zafri'))
        self.stdout.write(self.style.SUCCESS('Username: admin | Password: admin123'))