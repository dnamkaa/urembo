# Smart Retail System - Products Module Design
## Tanzania POS & Inventory Management Platform

---

## 1. DATABASE SCHEMA & DATA MODEL

### Products Table Structure

```sql
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    cost_price_tzs DECIMAL(12, 2) NOT NULL,
    selling_price_tzs DECIMAL(12, 2) NOT NULL,
    reorder_level INTEGER NOT NULL DEFAULT 10,
    description TEXT,
    image_url VARCHAR(500),
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE INDEX idx_sku ON products(sku);
CREATE INDEX idx_name ON products(name);
CREATE INDEX idx_category ON products(category);
CREATE INDEX idx_is_active ON products(is_active);
```

### Field Definitions & Retail Operations Justification

| Field | Type | Purpose | Retail Importance |
|-------|------|---------|-------------------|
| **product_id** | INT PK | Unique identifier | Database integrity & foreign key relationships |
| **sku** | VARCHAR(50) UNIQUE | Stock Keeping Unit | Core identifier for POS scanning, inventory tracking, supplier orders |
| **name** | VARCHAR(255) | Product display name | Customer receipts, shopping lists, reports |
| **category** | VARCHAR(100) | Product grouping | POS drawer organization, tax rules (VAT rates vary by category in TZ), analytics |
| **cost_price_tzs** | DECIMAL(12,2) | Cost to acquire product | Profit margin calculation, cost of goods sold (COGS), supplier invoicing |
| **selling_price_tzs** | DECIMAL(12,2) | Retail selling price | POS pricing, customer charging, revenue tracking |
| **reorder_level** | INT | Minimum stock threshold | Automatic low-stock alerts, purchase order triggers, stockout prevention |
| **description** | TEXT | Product details | Customer-facing info, packaging notes, allergen warnings, instructions |
| **image_url** | VARCHAR(500) | Product photo | POS display, online catalog, staff identification |
| **is_active** | BOOLEAN | Active status flag | Enables soft-delete (archive vs permanent delete), prevent accidental sales of discontinued items |
| **created_at** | TIMESTAMP | Creation timestamp | Audit trail, product age analysis, startup inventory reference |
| **updated_at** | TIMESTAMP | Last modification time | Track pricing changes, detect stale data, compliance reporting |

---

## 2. RWANDA MARKET CONSIDERATIONS

### Why This Design for Tanzania:

1. **Flexible SKU System**: Many Tanzanian retail shops lack barcode infrastructure. SKU can be:
   - Manual entry (e.g., "SOAP001", "RICE005")
   - Auto-generated (e.g., "SKU20260301001")
   - Phone number suffix (e.g., "PROD" + last 4 digits of phone)

2. **Price Ranges**: Tanzanian products span wide ranges:
   - Street vendor items: TZS 500–5,000
   - Supermarket goods: TZS 5,000–50,000
   - Premium/imported: TZS 50,000–500,000+

3. **Small-to-Medium Catalogs**: Most Tanzanian shops have 50–500 products:
   - Village shop: 50-100 items
   - Supermarket: 300-1000 items
   - Pharmacies: 100-300 items

4. **Reorder Levels**: Critical for capital-constrained shops (less working capital):
   - Prevents overstocking (cash flow preservation)
   - Alerts before stockouts (lost sales)
   - Suitable for supplier cycles (1–3 days in urban Tanzania)

5. **Cost vs Selling Price**: Essential for:
   - Profit tracking (many shop owners don't calculate margins)
   - VAT compliance (Tanzania has VAT on different product categories)
   - Supplier negotiations

6. **Image URLs**: Support both:
   - Local file uploads (no internet needed)
   - Cloud URLs (for connected shops)

7. **Soft-Delete (is_active)**: Safer than hard-delete:
   - Historical data preserved for reports
   - Prevents accidental data loss
   - Audit trail for compliance

---

## 3. REST API ENDPOINTS

### Product Operations

```
GET /api/v1/products
  Query Params: 
    - page (default: 1)
    - limit (default: 20, max: 100)
    - category (filter by category)
    - is_active (true/false, default: true)
  Response: 
    {
      "status": "success",
      "data": [
        {
          "product_id": 1,
          "sku": "SKU20260301001",
          "name": "Omo Detergent 1kg",
          "category": "Home Care",
          "cost_price_tzs": 4500,
          "selling_price_tzs": 5500,
          "margin_percent": 22.22,
          "reorder_level": 20,
          "description": "Quality detergent for clothes",
          "image_url": "https://...",
          "is_active": true,
          "created_at": "2026-03-01T10:30:00Z"
        }
      ],
      "pagination": {
        "total": 250,
        "page": 1,
        "limit": 20,
        "total_pages": 13
      }
    }

POST /api/v1/products
  Body: {
    "sku": "SKU20260301002",  // Optional, auto-generate if not provided
    "name": "Coca Cola 500ml",
    "category": "Beverages",
    "cost_price_tzs": 1800,
    "selling_price_tzs": 2500,
    "reorder_level": 50,
    "description": "Carbonated soft drink",
    "image_url": "https://...",
    "is_active": true
  }
  Response: {
    "status": "success",
    "data": { product object with auto-generated product_id }
  }

GET /api/v1/products/{product_id}
  Response: { single product object }

PUT /api/v1/products/{product_id}
  Body: { fields to update }
  Response: { updated product object }

DELETE /api/v1/products/{product_id}
  Response: { "status": "success", "message": "Product archived" }
  Note: Soft-delete (sets is_active=false)

GET /api/v1/products/search?q=coca
  Query Params:
    - q (search term)
    - fields (comma-separated: name, sku, category)
  Response: { matching products array }

GET /api/v1/products/category/{category}
  Response: { products filtered by category }

GET /api/v1/products/low-stock
  Response: { products below reorder_level }

POST /api/v1/products/bulk-upload
  Body: FormData with Excel file
  Response: { 
    "status": "success",
    "imported": 45,
    "errors": [ { row: 5, error: "Duplicate SKU" } ]
  }

GET /api/v1/products/stats
  Response: {
    "total_products": 250,
    "active_products": 245,
    "low_stock_count": 12,
    "total_cost_value_tzs": 5250000,
    "total_selling_value_tzs": 6875000
  }
```

---

## 4. TANZANIA RETAIL EXAMPLE DATA

### Example Products for Tanzanian Market

```json
[
  {
    "sku": "SOAP001",
    "name": "Lux White Soap 100g",
    "category": "Personal Care",
    "cost_price_tzs": 1200,
    "selling_price_tzs": 1500,
    "reorder_level": 50,
    "description": "Premium white soap for daily use",
    "image_url": "images/lux-soap.jpg",
    "is_active": true
  },
  {
    "sku": "RICE001",
    "name": "Pishori Rice 2kg",
    "category": "Grains",
    "cost_price_tzs": 3500,
    "selling_price_tzs": 4200,
    "reorder_level": 30,
    "description": "Premium basmati-style rice",
    "image_url": "images/pishori-rice.jpg",
    "is_active": true
  },
  {
    "sku": "OIL001",
    "name": "Sunflower Oil 1L",
    "category": "Cooking",
    "cost_price_tzs": 5500,
    "selling_price_tzs": 6800,
    "reorder_level": 20,
    "description": "Pure refined sunflower oil",
    "image_url": "images/sunflower-oil.jpg",
    "is_active": true
  },
  {
    "sku": "FLOUR001",
    "name": "Wheat Flour 2kg",
    "category": "Grains",
    "cost_price_tzs": 2800,
    "selling_price_tzs": 3500,
    "reorder_level": 40,
    "description": "PRO flour for baking",
    "image_url": "images/pro-flour.jpg",
    "is_active": true
  },
  {
    "sku": "SALT001",
    "name": "Everta Salt 500g",
    "category": "Spices",
    "cost_price_tzs": 500,
    "selling_price_tzs": 800,
    "reorder_level": 100,
    "description": "Iodized salt with anti-caking",
    "image_url": "images/everta-salt.jpg",
    "is_active": true
  },
  {
    "sku": "SUGAR001",
    "name": "Sukari Refined Sugar 1kg",
    "category": "Sweeteners",
    "cost_price_tzs": 2200,
    "selling_price_tzs": 2800,
    "reorder_level": 30,
    "description": "Pure white refined sugar",
    "image_url": "images/sugar.jpg",
    "is_active": true
  },
  {
    "sku": "MILK001",
    "name": "Ushindi Milk Powder 400g",
    "category": "Dairy",
    "cost_price_tzs": 7500,
    "selling_price_tzs": 9500,
    "reorder_level": 25,
    "description": "Fortified full cream milk powder",
    "image_url": "images/ushindi-milk.jpg",
    "is_active": true
  },
  {
    "sku": "TEA001",
    "name": "Brooke Bond Tanganyika Tea 50g",
    "category": "Beverages",
    "cost_price_tzs": 6500,
    "selling_price_tzs": 8000,
    "reorder_level": 35,
    "description": "Premium loose leaf black tea",
    "image_url": "images/brooke-bond-tea.jpg",
    "is_active": true
  },
  {
    "sku": "SUGAR_DRINK001",
    "name": "Coca Cola 400ml Bottle",
    "category": "Soft Drinks",
    "cost_price_tzs": 1400,
    "selling_price_tzs": 2000,
    "reorder_level": 60,
    "description": "Carbonated soft drink",
    "image_url": "images/coca-cola.jpg",
    "is_active": true
  },
  {
    "sku": "JUICE001",
    "name": "Minute Maid Orange Juice 200ml",
    "category": "Beverages",
    "cost_price_tzs": 1200,
    "selling_price_tzs": 1800,
    "reorder_level": 50,
    "description": "Orange juice concentrate",
    "image_url": "images/minute-maid.jpg",
    "is_active": true
  }
]
```

---

## 5. SYSTEM ARCHITECTURE

### Technology Stack

**Backend:**
- Framework: Flask (Python)
- Database: SQLite (small shops) or PostgreSQL (scaling)
- ORM: SQLAlchemy
- Validation: Marshmallow
- File Upload: Flask-Upload / Werkzeug

**Frontend:**
- Framework: HTML5 + Bootstrap 5
- Interactivity: JavaScript / AJAX
- Charts: Chart.js
- Image Gallery: Lightbox.js

**Additional Services (Phase 2):**
- Authentication: JWT tokens
- File Storage: Cloud storage (AWS S3 / Google Cloud)
- Barcode Generation: python-barcode
- Excel Processing: openpyxl

---

## 6. DESIGN DECISIONS & RATIONALE

### Why Decimal(12,2) for Prices?
- Supports up to 9,999,999.99 TZS (covers retail range)
- Precise to 2 decimal places (cents/minor units)
- Prevents floating-point rounding errors
- Standard in financial systems

### Why Soft-Delete?
- Preserves historical data for reporting
- Prevents accidental permanent loss
- Enables product "revival" if needed
- Audit trail for compliance
- Simpler than complex hard-delete cascades

### Why Separate Cost & Selling Price?
- Enables profit margin calculation
- Supports pricing strategies
- Critical for financial reporting (COGS, GP%)
- Helps identify unprofitable products
- Tanzania VAT rules may differ by margin

### Why Reorder Level?
- Tanzanian shops operate with limited capital
- Prevents overstocking (cash flow critical)
- Alerts for timely supplier orders (1–3 day cycles)
- Reduces lost sales from stockouts
- Useful for small shops without demand forecasting

### Why Image URL (not Local Storage)?
- Reduces server storage costs
- Enables scaling to cloud storage later
- Better performance (CDN capable)
- Supports both local and remote images

### Why Categories?
- POS drawer organization (quick access)
- Tax categorization (Tanzania has different VAT rates)
- Stock filtering by department
- Enables category-level analytics
- Supports supplier grouping

---

## 7. IMPLEMENTATION ROADMAP

### Phase 1: Core Product Management (Current Sprint)
- ✓ Database schema
- ✓ CRUD API endpoints
- ✓ Frontend: Product list, Add, Edit, View
- ✓ Search & filtering
- ✓ Low stock indicator

### Phase 2: Advanced Features
- Bulk Excel upload
- Barcode generation & scanning
- Product images (local file upload)
- SKU auto-generation
- Advanced analytics

### Phase 3: Integration with Other Modules
- Inventory tracking
- POS sales system
- Supplier management
- Profit analytics

---
