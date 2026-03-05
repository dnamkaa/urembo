# Reports & Analytics Module - Complete Documentation

## Overview

The **Reports & Analytics Module** provides comprehensive business intelligence for the Smart Retail System, enabling owners to monitor sales performance, track top products, and maintain inventory health.

All monetary amounts are in **TZS (Tanzanian Shillings)** as integers (no decimals).

---

## API Endpoints

### 1. Dashboard KPIs

```
GET /api/reports/dashboard?date=YYYY-MM-DD
```

**Query Parameters:**
- `date` (optional): Date to report on (defaults to today). Format: YYYY-MM-DD

**Response:**
```json
{
  "status": "success",
  "date": "2026-03-05",
  "today": {
    "total_sales_tzs": 97500,
    "transactions": 3,
    "avg_basket_tzs": 32500
  },
  "week": {
    "total_sales_tzs": 97500,
    "transactions": 3
  },
  "month": {
    "total_sales_tzs": 97500,
    "transactions": 3
  },
  "inventory": {
    "low_stock_count": 1,
    "out_of_stock_count": 0
  }
}
```

**KPI Definitions:**
- **today.total_sales_tzs**: Sum of total_tzs for all PAID sales today
- **today.transactions**: Count of PAID sales today
- **today.avg_basket_tzs**: Average transaction value (total_sales / transactions)
- **week.total_sales_tzs**: Sum of all PAID sales this week (Monday to today)
- **month.total_sales_tzs**: Sum of all PAID sales this month
- **inventory.low_stock_count**: Products below their reorder_level
- **inventory.out_of_stock_count**: Products with zero current_stock

**Business Logic:**
- Only PAID sales are counted (VOIDED, FAILED, PENDING excluded)
- Stock calculated from `SUM(inventory_movements)` grouped by `sku`
- Week starts on Monday
- Month starts on day 1

---

### 2. Sales Report

```
GET /api/reports/sales?from=YYYY-MM-DD&to=YYYY-MM-DD
```

**Query Parameters:**
- `from` (optional): Start date. Defaults to 30 days ago
- `to` (optional): End date. Defaults to today

**Response:**
```json
{
  "status": "success",
  "from": "2026-02-03",
  "to": "2026-03-05",
  "total_revenue_tzs": 97500,
  "total_transactions": 3,
  "daily": [
    {
      "date": "2026-03-05",
      "total_tzs": 97500,
      "transactions": 3
    }
  ],
  "payment_methods": [
    {
      "method": "CASH",
      "total_tzs": 67500,
      "transactions": 2
    },
    {
      "method": "MOBILE_MONEY",
      "total_tzs": 30000,
      "transactions": 1
    }
  ]
}
```

**Features:**
- Daily breakdown of sales
- Payment method breakdown (CASH, MOBILE_MONEY, CARD, BANK_TRANSFER)
- Includes only PAID sales
- CSV export support from UI

---

### 3. Top Products

```
GET /api/reports/top-products?from=YYYY-MM-DD&to=YYYY-MM-DD&by=qty|revenue&limit=20
```

**Query Parameters:**
- `from` (optional): Start date. Defaults to 30 days ago
- `to` (optional): End date. Defaults to today
- `by` (optional): Sort method. `qty` or `revenue`. Defaults to `revenue`
- `limit` (optional): Maximum results. Defaults to 20, max 100

**Response:**
```json
{
  "status": "success",
  "from": "2026-02-03",
  "to": "2026-03-05",
  "by": "revenue",
  "count": 5,
  "products": [
    {
      "sku": "SOAP001",
      "name": "Safeguard Soap",
      "qty_sold": 10,
      "revenue_tzs": 30000
    },
    {
      "sku": "OIL001",
      "name": "Cooking Oil 1L",
      "qty_sold": 5,
      "revenue_tzs": 30000
    }
  ]
}
```

**Calculations:**
- **qty_sold**: Sum of all quantity in sale_items for product
- **revenue_tzs**: Sum of line_total_tzs for product
- Only PAID sales counted

---

### 4. Inventory Health

```
GET /api/reports/inventory-health
```

**No Parameters**

**Response:**
```json
{
  "status": "success",
  "low_stock": {
    "count": 1,
    "items": [
      {
        "sku": "BREAD001",
        "name": "White Bread",
        "category": "Bakery",
        "current_stock": 4,
        "reorder_level": 20,
        "units_to_reorder": 16
      }
    ]
  },
  "out_of_stock": {
    "count": 0,
    "items": []
  },
  "inventory_value_estimate_tzs": 468200
}
```

**Calculations:**
- **current_stock**: `SUM(quantity WHERE movement_type IN [STOCK_IN, ADJUSTMENT, RETURN]) - SUM(quantity WHERE movement_type IN [SALE, TRANSFER_OUT])`
- **units_to_reorder**: `MAX(0, reorder_level - current_stock)`
- **inventory_value_estimate_tzs**: `SUM(cost_price_tzs * current_stock)` for all active products

**Categorization:**
- **out_of_stock**: current_stock == 0
- **low_stock**: 0 < current_stock < reorder_level

---

## Database Query Examples

### Total Sales for Date Range (Revenue Report)

```python
from datetime import datetime

from_date = datetime.strptime('2026-03-01', '%Y-%m-%d')
to_date = datetime.strptime('2026-03-05', '%Y-%m-%d').replace(hour=23,minute=59,second=59)

sales = Sale.query.filter(
    Sale.payment_status == 'PAID',
    Sale.sale_datetime >= from_date,
    Sale.sale_datetime <= to_date
).all()

total_revenue = sum(s.total_tzs for s in sales)
```

### Top Products by Revenue

```python
sales = Sale.query.filter(
    Sale.payment_status == 'PAID',
    Sale.sale_datetime >= from_date,
    Sale.sale_datetime <= to_date
).all()

product_data = {}
for sale in sales:
    for item in sale.items:
        sku = item.sku
        if sku not in product_data:
            product_data[sku] = {
                'sku': item.sku,
                'name': item.product_name_snapshot,
                'qty_sold': 0,
                'revenue_tzs': 0
            }
        product_data[sku]['qty_sold'] += item.qty
        product_data[sku]['revenue_tzs'] += item.line_total_tzs

# Sort by revenue descending
top_products = sorted(
    product_data.values(),
    key=lambda x: x['revenue_tzs'],
    reverse=True
)[:20]
```

### Low Stock Items

```python
low_stock_items = []

for product in Product.query.filter_by(is_active=True).all():
    current_stock = product.get_current_stock()
    
    if 0 < current_stock < product.reorder_level:
        low_stock_items.append({
            'sku': product.sku,
            'name': product.name,
            'current_stock': current_stock,
            'reorder_level': product.reorder_level,
            'units_to_reorder': product.reorder_level - current_stock
        })

# Sort by units_to_reorder descending
low_stock_items.sort(key=lambda x: x['units_to_reorder'], reverse=True)
```

### Inventory Value Estimate

```python
inventory_value = 0

for product in Product.query.filter_by(is_active=True).all():
    current_stock = product.get_current_stock()
    cost_price = int(float(product.cost_price_tzs))
    inventory_value += cost_price * current_stock
```

---

## UI Pages

### 1. Dashboard (/reports/dashboard)

**Features:**
- 6 KPI cards (Today Sales, Avg Basket, Week Sales, Month Sales, Out of Stock, Low Stock)
- Auto-refresh capability
- Inventory alerts if items are low or out of stock
- Color-coded alerts (Red for critical, Yellow for warning, Green for healthy)

**Components:**
- KPI Grid: Responsive 6-column layout
- Alert Cards: Summary warnings and good health messages
- Refresh Button: Manual refresh with loading spinner

### 2. Sales Report (/reports/sales)

**Features:**
- Date range filters (from/to dates)
- Daily sales summary table
- Payment method breakdown table
- CSV export functionality
- Summary cards (Total Revenue, Transaction Count)

**Tables:**
1. **Daily Sales Summary**
   - Date
   - Total Sales (TZS)
   - Transaction Count

2. **Payment Method Breakdown**
   - Payment Method
   - Total Sales (TZS)
   - Transaction Count

### 3. Top Products (/reports/top-products)

**Features:**
- Date range filters
- Sort by Revenue or Quantity Sold
- Ranking with numbered badges
- Product details (SKU, Name, Qty/Revenue)

**Columns:**
- Rank (1, 2, 3... in colored circle)
- SKU
- Product Name
- Quantity Sold or Revenue (depending on sort)

### 4. Inventory Health (/reports/inventory-health)

**Features:**
- Inventory Value Estimate card (large, green, prominent)
- Low Stock Items section (with units to reorder)
- Out of Stock Items section (critical alert)
- Auto-refresh capability

**Tables:**
1. **Out of Stock Items**
   - SKU, Name, Category, Reorder Level

2. **Low Stock Items**
   - SKU, Name, Category, Current Stock, Reorder Level, Units to Reorder

---

## Performance Optimization

### Recommended Indexes

```sql
-- Sales table
CREATE INDEX idx_sales_status_date ON sales(payment_status, sale_datetime);
CREATE INDEX idx_sales_datetime ON sales(sale_datetime);

-- Sale Items table
CREATE INDEX idx_sale_items_sale_id ON sale_items(sale_id);
CREATE INDEX idx_sale_items_sku ON sale_items(sku);

-- Inventory Movements table
CREATE INDEX idx_movements_sku_date ON inventory_movements(sku, created_at);
CREATE INDEX idx_movements_sku_type ON inventory_movements(sku, movement_type);
```

### Query Performance

- **Dashboard KPIs**: Full scan of sales table filtered by date and status (fast with indexes)
- **Sales Report**: Full scan of sales table for date range (optimal with date index)
- **Top Products**: Full scan of sale_items + aggregation (optimization possible with materialized view)
- **Inventory Health**: Full scan of products + per-product stock calculation (scales well up to 10k products)

**Expected Query Times:**
- Dashboard: <100ms
- Sales Report: <200ms 
- Top Products: <300ms
- Inventory Health: <400ms

For 100k+ sales records, consider:
- Pre-calculated daily summaries table
- Materialized view for top products
- Cached inventory values (refreshed hourly)

---

## Testing

Run the comprehensive test suite:

```bash
python tests_reports.py
```

**Test Coverage:**
- ✅ Dashboard KPI accuracy (today, week, month)
- ✅ Sales report breakdown (daily, payment methods)
- ✅ Top products by qty and revenue
- ✅ Inventory health (low stock, out of stock)
- ✅ VOIDED/FAILED sales excluded from revenue
- ✅ Currency values are integers
- ✅ All UI pages load correctly
- ✅ CSV export functionality
- ✅ Date range filtering
- ✅ Payment method breakdown sums correctly

**21 Total Tests** - All passing

---

## Data Integrity Rules

1. **Revenue Only Counts PAID Sales**
   - VOIDED: Customer returned goods or transaction was cancelled
   - FAILED: Payment failed
   - PENDING: Payment still pending
   - Only `payment_status = 'PAID'` counts toward revenue

2. **Stock Is Never Direct**
   - Products never have direct quantity edits
   - Stock = `SUM(inventory_movements)` where:
     - +qty for: STOCK_IN, ADJUSTMENT (add), RETURN
     - -qty for: SALE, TRANSFER_OUT, ADJUSTMENT (remove)

3. **Historical Snapshots Are Preserved**
   - sale_items.product_name_snapshot: Name at time of sale
   - sale_items.unit_price_tzs_snapshot: Price at time of sale
   - Cannot be modified after sale is recorded
   - Ensures accurate profit calculation even if product price changes

4. **Currency Is TZS Integers**
   - All amounts stored as integers (no decimal places)
   - 1500 TZS (not 15.00)
   - Eliminates floating-point precision issues
   - Suitable for Tanzanian market

5. **Audit Trail Is Complete**
   - No hard deletes (soft delete via payment_status = 'VOIDED')
   - All inventory changes tracked in inventory_movements
   - All sales tracked with receipt_no, date, cashier, method
   - Complete history for compliance and reconciliation

---

## Future Enhancements

1. **Profit Snapshots**
   - Add gross_profit_tzs to sales reports
   - Save profit at time of sale to match historical accuracy
   - Include margin percentages

2. **Cashier Performance**
   - Reports by cashier (sales count, avg basket, error rate)
   - Trend analysis (best performing hours/days)
   - Performance bonuses tracking

3. **Product Analytics**
   - Profit by product (using snapshot prices and cost)
   - Turnover rate per product
   - Demand forecasting
   - Trend analysis (moving averages, growth rates)

4. **Scheduled Reports**
   - Daily email reports (sales summary, alerts)
   - Weekly/monthly PDF reports
   - Automated low stock purchase orders
   - End-of-day reconciliation reports

5. **Advanced Filtering**
   - By cashier name
   - By product category
   - By customer (future loyalty module)
   - By payment method status (PAID/PENDING/FAILED)

6. **Data Export**
   - Excel (.xlsx) with multiple sheets
   - PDF reports with charts and graphics
   - JSON API for external BI tools
   - CSV with extended data

7. **Dashboards & Visualizations**
   - Sales trend charts (line graphs)
   - Category breakdowns (pie charts)
   - Payment method distribution (bar charts)
   - Inventory health heatmap

---

## Support & Troubleshooting

### Common Issues

**Issue: Reports show zero sales despite having PAID transactions**
- **Check:** Ensure sales have `payment_status = 'PAID'` (not 'PENDING', 'FAILED', 'VOIDED')
- **Check:** Verify sale_datetime is within the selected date range
- **Check:** View database: `SELECT * FROM sales WHERE payment_status = 'PAID'`

**Issue: Inventory value seems incorrect**
- **Check:** Verify all products have `cost_price_tzs` set
- **Check:** Verify inventory_movements are being recorded on checkout
- **Check:** Test individual product: `SELECT SUM(quantity) FROM inventory_movements WHERE sku='XXX'`

**Issue: Top products not showing all items sold**
- **Check:** Ensure all sales are PAID (voided sales excluded)
- **Check:** Verify sale_items are being created with product_name_snapshot
- **Check:** Review date range filter (defaults to 30 days)

**Issue: Stock levels wrong after checkout**
- **Check:** Verify SALE movements created on checkout
- **Check:** Verify no overlapping RETURN movements
- **Check:** Recalculate: `get_current_stock()` from fresh movements

---

## Assumptions & Limitations

1. **Single Currency (TZS)**: Multi-currency not supported; assume all prices in TZS
2. **Single Store**: Reports for entire system; no location filtering
3. **No Customer Profiles**: Reports by payment method only, not by individual customer
4. **Cost Price Static**: Uses current cost_price_tzs; historical cost not tracked separately
5. **No VAT/Tax Tracking**: Sales totals are inclusive of any tax
6. **Real-time Indexing**: Reports query live database; may be slow with 1M+ records
7. **No Multi-user Access Control**: All users see all reports; no role-based filtering
8. **No Predictive Analytics**: Reports are retrospective only, no forecasting

