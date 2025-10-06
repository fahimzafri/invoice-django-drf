import uuid
from django.db import models
from django.core.exceptions import ValidationError

class Invoice(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    )
    
    reference_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    customer_name = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.reference_number} for {self.customer_name}"

    def update_total_amount(self):
        """Recalculates the total amount from its items."""
        total = self.items.aggregate(total=models.Sum(models.F('quantity') * models.F('unit_price')))['total']
        self.total_amount = total or 0.00
        self.save(update_fields=['total_amount'])

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be positive.")
        if self.unit_price < 0:
            raise ValidationError("Unit price cannot be negative.")

    def __str__(self):
        return f"{self.description} ({self.quantity} x {self.unit_price})"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('Sale', 'Sale'),
        ('Payment', 'Payment'),
    )

    invoice = models.ForeignKey(Invoice, related_name='transactions', on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for Invoice {self.invoice.reference_number}"