from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Invoice, Transaction
from .serializers import InvoiceSerializer, TransactionSerializer
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.prefetch_related('items', 'transactions').all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        invoice = serializer.save()
        # Recalculate total from items
        invoice.update_total_amount()
        # Create a "Sale" transaction when an invoice is created
        Transaction.objects.create(
            invoice=invoice,
            transaction_type='Sale',
            amount=invoice.total_amount
        )

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        invoice = self.get_object()
        
        if invoice.status == 'Paid':
            return Response({'error': 'Invoice is already paid.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update invoice status
        invoice.status = 'Paid'
        invoice.save()
        
        # Create a "Payment" transaction
        Transaction.objects.create(
            invoice=invoice,
            transaction_type='Payment',
            amount=invoice.total_amount
        )
        
        return Response(self.get_serializer(invoice).data)
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]