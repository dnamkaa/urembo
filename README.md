# Smart Retail System - Products Module
## Tanzania POS & Inventory Management Platform

**Version:** 1.0  
**Status:** Development (Phase 1: Products Module)  
**Target Market:** Tanzania (Currency: TZS - Tanzania Shillings)

---

## 📦 What is Smart Retail System?

A modern web-based **Point of Sale (POS)** and **Inventory Management** system designed specifically for Tanzanian retail shops, supermarkets, and pharmacies.

### Why Built for Tanzania?
- ✅ Support for flexible SKU systems (no barcode requirement)
- ✅ Price ranges suitable for Tanzanian economy (500 TZS - 500,000+ TZS)
- ✅ Small-to-medium catalog support (50-2000 products)
- ✅ Profit margin calculations (critical for shop owners)
- ✅ Reorder level management (cash flow management)
- ✅ Works online and offline

---

## 🎯 Phase 1: Products Module (Current)

**Status:** ✅ Complete & Ready to Test

This module provides complete product management functionality:

### Features Implemented

#### 1. Product CRUD Operations
- **Create** products with auto-generated SKUs
- **Read** product details with profit calculations
- **Update** product information anytime
- **Delete** (soft-delete via archiving) products

#### 2. Product Data Model
```
product_id (ID)
├── sku (Unique identifier)
├── name (Product name)
├── category (Product group)
├── cost_price_tzs (Cost in TZS)
├── selling_price_tzs (Selling price in TZS)
├── margin_percent (Calculated)
├── reorder_level (Stock alert threshold)
├── description (Product details)
├── image_url (Product photo)
├── is_active (Status)
├── created_at (Timestamp)
└── updated_at (Timestamp)
```

#### 3. REST API Endpoints
- `GET /api/v1/products` - List all products (paginated)
- `GET /api/v1/products/{id}` - Get single product
- `POST /api/v1/products` - Create new product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Archive product
- `GET /api/v1/products/search?q=term` - Search products
- `GET /api/v1/products/category/{name}` - Filter by category
- `GET /api/v1/products/stats` - Statistics
- `GET /api/v1/categories` - List all categories

#### 4. Web UI Features
- **Dashboard** - Overview with statistics
- **Product List** - Browse all products with search & filter
- **Add Product** - Create new product with real-time margin calculation
- **Edit Product** - Update existing product
- **Quick View** - See product details
- **Category Management** - Organize products
- **Price Guide** - Suggested margins by category

---

## 🚀 Quick Start Guide

### System Requirements
- Python 3.8+
- Windows/Mac/Linux
- ~200MB disk space

### Installation Steps

#### 1. Clone or Download
```bash
cd c:\Users\knamk\Desktop\urembo
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
```

#### 3. Activate Virtual Environment

**Windows:**
```bash
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
source .venv/bin/activate
```

#### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Initialize Database & Seed Sample Data
```bash
python
>>> from app import app, init_db, seed_sample_data
>>> with app.app_context():
...     init_db()
...     seed_sample_data()
... exit()
```

#### 6. Run the Application
```bash
python app.py
```

**Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

#### 7. Open in Browser
```
http://127.0.0.1:5000
```

---

## 📊 Sample Products (Tanzania Market)

The system comes pre-loaded with 10 sample Tanzanian retail products:

| SKU | Product | Category | Cost (TZS) | Price (TZS) | Margin |
|-----|---------|----------|------------|-------------|---------|
| SOAP001 | Lux White Soap 100g | Personal Care | 1,200 | 1,500 | 25% |
| RICE001 | Pishori Rice 2kg | Grains | 3,500 | 4,200 | 20% |
| OIL001 | Sunflower Oil 1L | Cooking | 5,500 | 6,800 | 24% |
| FLOUR001 | PRO Wheat Flour 2kg | Grains | 2,800 | 3,500 | 25% |
| SALT001 | Everta Salt 500g | Spices | 500 | 800 | 60% |
| SUGAR001 | Sukari Sugar 1kg | Sweeteners | 2,200 | 2,800 | 27% |
| MILK001 | Ushindi Milk Powder 400g | Dairy | 7,500 | 9,500 | 27% |
| TEA001 | Brooke Bond Tea 50g | Beverages | 6,500 | 8,000 | 23% |
| COKE001 | Coca Cola 400ml | Soft Drinks | 1,400 | 2,000 | 43% |
| JUICE001 | Minute Maid Juice 200ml | Beverages | 1,200 | 1,800 | 50% |

---

## 🔌 API Usage Examples

### 1. Get All Products
```bash
curl http://127.0.0.1:5000/api/v1/products
```

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "product_id": 1,
      "sku": "SOAP001",
      "name": "Lux White Soap 100g",
      "category": "Personal Care",
      "cost_price_tzs": 1200,
      "selling_price_tzs": 1500,
      "margin_percent": 25.0,
      "reorder_level": 50,
      "description": "Premium white soap for daily use",
      "image_url": "https://...",
      "is_active": true,
      "created_at": "2026-03-04T10:30:00"
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "limit": 20,
    "total_pages": 1
  }
}
```

### 2. Search Products
```bash
curl "http://127.0.0.1:5000/api/v1/products/search?q=soap"
```

### 3. Get Categories
```bash
curl http://127.0.0.1:5000/api/v1/categories
```

**Response:**
```json
{
  "status": "success",
  "data": ["Personal Care", "Grains", "Cooking", "Spices", ...]
}
```

### 4. Create Product
```bash
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Product",
    "category": "Beverages",
    "cost_price_tzs": 5000,
    "selling_price_tzs": 7500,
    "reorder_level": 25,
    "description": "Product details"
  }'
```

**Response:**
```json
{
  "status": "success",
  "message": "Product created",
  "data": {
    "product_id": 11,
    "sku": "SKU-20260304133042-01",
    "name": "New Product",
    ...
  }
}
```

### 5. Update Product
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "selling_price_tzs": 1800
  }'
```

### 6. Get Statistics
```bash
curl http://127.0.0.1:5000/api/v1/products/stats
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_products": 10,
    "active_products": 10,
    "archived_products": 0,
    "total_cost_value_tzs": 34200,
    "total_selling_value_tzs": 44200,
    "average_margin_percent": 29.15
  }
}
```

---

## 🏗️ Architecture Overview

### Technology Stack
- **Backend:** Flask 2.3+ (Python web framework)
- **Database:** SQLite 3 (embedded, lightweight)
- **ORM:** SQLAlchemy 2.0+ (SQL toolkit & ORM)
- **Frontend:** HTML5 + Bootstrap 5 + JavaScript
- **Server:** Built-in Flask dev server (for development)

### File Structure
```
urembo/
├── app.py                    # Main Flask application & models
├── requirements.txt          # Python dependencies
├── run.py                    # Startup script
├── SYSTEM_DESIGN.md         # System documentation
├── README.md                # This file
├── smart_retail.db          # SQLite database (auto-created)
└── templates/
    ├── base.html            # Base template with navbar
    ├── index.html           # Dashboard
    └── products/
        ├── list.html        # Product list & search
        ├── form.html        # Add/edit product form
        └── view.html        # Product details view
```

### Database Schema
```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE,
    name VARCHAR(255),
    category VARCHAR(100),
    cost_price_tzs DECIMAL(12,2),
    selling_price_tzs DECIMAL(12,2),
    reorder_level INTEGER,
    description TEXT,
    image_url VARCHAR(500),
    is_active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 🎨 UI Screenshots & Walkthrough

### Dashboard
- Purpose: Overview of product inventory
- Shows: Total products, categories, cost value, average margin
- Quick actions: Add product, refresh stats
- Recent products: Latest 10 products with margins

### Products List Page
- Search bar: Find by name or SKU
- Category filter: Filter by product group
- Product table with:
  - SKU (unique identifier)
  - Name & description
  - Category badge
  - Cost & selling prices in TZS
  - Profit margin percentage
  - Edit/Delete actions
- Pagination: Browse pages of products

### Add/Edit Product Form
- SKU: Manual entry or auto-generate
- Name: Product name
- Category: Select from common categories or custom
- Prices: Cost and selling price (in TZS)
- Real-time margin calculation
- Reorder level: Stock alert threshold
- Description: Product details
- Image URL: Link to product photo
- Price guide: Category suggestions for margins

---

## 📈 Tanzania Retail Market Notes

### Typical Shop Configurations
1. **Village Shop (Duka)**
   - 50-100 products
   - Owner-operated
   - Limited capital
   - Daily cash reconciliation

2. **Supermarket**
   - 300-1000 products
   - Multiple staff
   - Daily inventory checks
   - Complex pricing (multi-tier)

3. **Pharmacy**
   - 100-300 products
   - Strict stock management
   - Regulatory requirements
   - High profit margins (40-100%)

### Price Range Guidelines
- **Essential items:** 500 - 5,000 TZS
- **Packaged goods:** 5,000 - 50,000 TZS
- **Premium/Imported:** 50,000 - 500,000+ TZS

### Typical Profit Margins (% of cost)
- Personal care: 20-30%
- Grains: 15-25%
- Cooking oils: 20-25%
- Beverages: 25-50%
- Dairy: 20-30%
- Spices: 40-80%
- Pharmacy items: 40-100%

---

## 🔐 Security Considerations

### Current Implementation (Development)
- No authentication (development mode)
- Debug mode enabled
- No input sanitization

### Production Recommendations (Phase 2)
- [ ] Add user authentication (JWT/session)
- [ ] Role-based access control (Admin, Staff, Manager)
- [ ] Input validation & sanitization
- [ ] HTTPS encryption
- [ ] Rate limiting on API
- [ ] Audit logging
- [ ] Data backup strategy

---

## 🚧 Roadmap - Future Phases

### Phase 2: Inventory Management (Planned)
- Stock tracking & transfers
- Low stock alerts
- Inventory adjustments
- Barcode scanning
- Stock reconciliation

### Phase 3: POS Sales System (Planned)
- Point of sale checkout
- Multiple payment methods (cash, mobile money)
- Receipt printing
- Sales tracking
- Discount management

### Phase 4: Reports & Analytics (Planned)
- Sales reports
- Profit analytics
- Best-selling products
- Inventory value reports
- Tax/VAT reporting (Tanzanian compliance)

---

## 🛠️ Troubleshooting

### Issue: Port 5000 already in use
**Solution:**
```bash
# Find and kill the process
lsof -i :5000
kill -9 <PID>

# Or use a different port
python app.py --port 5001
```

### Issue: Database locked error
**Solution:**
```bash
# Remove the old database
rm smart_retail.db

# Run the app to recreate it
python app.py
```

### Issue: Virtual environment not working
**Solution:**
```bash
# Recreate the virtual environment
rm -rf .venv
python -m venv .venv
# Activate and install
```

---

## 📚 Developer Guide

### Adding a New Field to Product
1. Update the Product model in `app.py`
2. Add new route/API endpoint if needed
3. Update templates if UI change needed
4. Create database migration (or delete smart_retail.db to reset)

### Example: Add SKU Prefix (e.g., "TZ-SHOP-001")
```python
# In app.py, modify generate_sku():
def generate_sku():
    now = datetime.utcnow()
    timestamp = now.strftime('%Y%m%d%H%M%S')
    count = Product.query.filter(
        Product.created_at >= now.replace(microsecond=0)
    ).count()
    return f'TZ-SHOP-{timestamp}-{str(count + 1).zfill(2)}'
```

### Adding a New API Endpoint
```python
@app.route('/api/v1/products/by-profit', methods=['GET'])
def api_products_by_profit():
    """Return products sorted by profit margin"""
    products = Product.query.filter_by(is_active=True).all()
    sorted_products = sorted(
        products,
        key=lambda p: float(p.selling_price_tzs) - float(p.cost_price_tzs),
        reverse=True
    )
    return jsonify({
        'status': 'success',
        'data': [p.to_dict() for p in sorted_products]
    }), 200
```

---

## 📞 Support & Contribution

This is an open-source project built for Tanzania's retail market.

### Ways to Contribute
- Report bugs
- Suggest features for Tanzania market
- Add translations (Swahili interface)
- Improve documentation
- Share real shop usage feedback

---

## 📄 License

Open Source - MIT License

---

## 👨‍💼 Built For

**Tanzanian Retail Businesses:**
- Small shops & dukas
- Supermarkets
- Pharmacies
- Restaurants
- Traders
- Wholesalers

**Currency:** TZS (Tanzania Shillings) 🇹🇿

**Language:** English (Swahili version coming in Phase 2)

---

## 🧪 Testing on GitHub

This project includes automated tests that run on every push and pull request to GitHub.

### GitHub Actions Workflow
- **Location:** `.github/workflows/tests.yml`
- **Trigger:** Automatic on push to `main` or `develop` branches, and pull requests
- **Runs:** Python 3.9, 3.10, 3.11
- **Time:** ~2-3 minutes per test suite

### View Test Results
1. Go to your GitHub repository
2. Click **Actions** tab
3. Select the latest workflow run
4. View the test output for each Python version

### Test Suites Included

#### POS Module Tests (17 tests)
```bash
python -m unittest tests_pos.TestPOSSalesModule -v
```
**Tests:**
- Product search and filtering
- Add to cart functionality
- Quantity updates
- Stock validation
- Discount validation
- Checkout workflow
- Payment method selection
- Receipt generation
- Sale void operations
- Inactive product handling

#### Reports Module Tests (21 tests)
```bash
python -m unittest tests_reports.ReportsTestCase -v
```
**Tests:**
- Dashboard KPI calculations
- Daily sales breakdown
- Payment method breakdown
- Top products ranking (by quantity & revenue)
- Inventory health reports
- Low/out-of-stock detection
- VOIDED sale exclusion
- PAID sale filtering
- Date range filtering
- CSV export

### Run Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
python -m unittest discover -v

# Run specific test suite
python -m unittest tests_pos.TestPOSSalesModule -v
python -m unittest tests_reports.ReportsTestCase -v

# Run specific test
python -m unittest tests_pos.TestPOSSalesModule.test_1_product_search -v
```

### Test Database
- Uses in-memory SQLite (`sqlite:///:memory:`)
- Fresh database for each test
- No side effects or data persistence
- Isolated temporary files per test

### Continuous Integration Benefits
✅ Automatic test runs on every commit  
✅ Prevents broken code from merging  
✅ Test results visible in PR checks  
✅ Multi-version Python compatibility verified  
✅ Build status badge available for README  

---

## 🎉 Getting Started
1. Follow the **Quick Start Guide** above
2. Open http://127.0.0.1:5000 in your browser
3. Browse the dashboard & products list
4. Try creating, editing, deleting products
5. Test the API endpoints
6. Read the SYSTEM_DESIGN.md for technical details

**Happy selling! 🛍️**

---

**Last Updated:** March 4, 2026  
**Version:** 1.0 (Products Module - Phase 1)
