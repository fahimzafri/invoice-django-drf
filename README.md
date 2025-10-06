# Invoice Management System

A Django REST Framework-based invoice management system with transaction tracking.

## Features

- Create, update, view, and manage invoices
- Auto-calculate invoice totals from items
- Track transactions (Sale/Payment)
- JWT authentication
- Mark invoices as paid

## Setup

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   cd invoice_project
   python manage.py migrate
   ```

5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh access token

### Invoices
- `GET /api/invoices/` - List all invoices
- `POST /api/invoices/` - Create new invoice
- `GET /api/invoices/{id}/` - Get invoice details
- `PUT /api/invoices/{id}/` - Update invoice
- `DELETE /api/invoices/{id}/` - Delete invoice
- `POST /api/invoices/{id}/pay/` - Mark invoice as paid

### Transactions
- `GET /api/transactions/` - List all transactions
- `GET /api/transactions/{id}/` - Get transaction details

## Usage Examples

### 1. Get Access Token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'
```

### 2. Create Invoice
```bash
curl -X POST http://127.0.0.1:8000/api/invoices/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "items": [
      {"description": "Product A", "quantity": 2, "unit_price": "50.00"},
      {"description": "Product B", "quantity": 1, "unit_price": "100.00"}
    ]
  }'
```

### 3. Mark Invoice as Paid
```bash
curl -X POST http://127.0.0.1:8000/api/invoices/1/pay/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Running Tests
```bash
python manage.py test
```
## Database Schema
┌─────────────────────────────────────┐
│         core_invoice                │
├─────────────────────────────────────┤
│ • id (PK)                           │
│ • reference_number (UNIQUE)         │
│ • customer_name                     │
│ • date                              │
│ • status (Pending/Paid)             │
│ • total_amount                      │
└─────────────┬───────────────────────┘
              │
              │ ONE-TO-MANY
              │
      ┌───────┴────────┐
      │                │
      ▼                ▼
┌─────────────────┐  ┌─────────────────────┐
│ core_invoiceitem│  │ core_transaction    │
├─────────────────┤  ├─────────────────────┤
│ • id (PK)       │  │ • id (PK)           │
│ • invoice_id(FK)│  │ • invoice_id (FK)   │
│ • description   │  │ • transaction_type  │
│ • quantity      │  │ • amount            │
│ • unit_price    │  │ • date              │
└─────────────────┘  └─────────────────────┘
