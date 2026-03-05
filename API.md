# Smart Retail System - API Documentation
## Products Module REST API

**Base URL:** `http://127.0.0.1:5000/api/v1`  
**Version:** 1.0  
**Content-Type:** `application/json`

---

## 📋 Table of Contents
1. [Products](#products)
2. [Search & Filter](#search--filter)
3. [Categories](#categories)
4. [Statistics](#statistics)
5. [Error Handling](#error-handling)
6. [Examples](#examples)

---

## Products

### List All Products

```http
GET /products
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | integer | 1 | Page number |
| limit | integer | 20 | Items per page (max 100) |
| category | string | null | Filter by category |
| is_active | boolean | true | Filter by status |

**Example Request:**
```bash
GET /api/v1/products?page=1&limit=20&category=Personal%20Care
```

**Success Response (200):**
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
      "image_url": "https://via.placeholder.com/200?text=Lux+Soap",
      "is_active": true,
      "created_at": "2026-03-04T10:30:00"
    }
  ],
  "pagination": {
    "total": 250,
    "page": 1,
    "limit": 20,
    "total_pages": 13
  }
}
```

---

### Get Single Product

```http
GET /products/{product_id}
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| product_id | integer | Product ID |

**Example Request:**
```bash
GET /api/v1/products/1
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": {
    "product_id": 1,
    "sku": "SOAP001",
    "name": "Lux White Soap 100g",
    "category": "Personal Care",
    "cost_price_tzs": 1200,
    "selling_price_tzs": 1500,
    "margin_percent": 25.0,
    "reorder_level": 50,
    "description": "Premium white soap for daily use",
    "image_url": "https://via.placeholder.com/200?text=Lux+Soap",
    "is_active": true,
    "created_at": "2026-03-04T10:30:00",
    "updated_at": "2026-03-04T10:35:00"
  }
}
```

**Error Response (404):**
```json
{
  "status": "error",
  "message": "Not found"
}
```

---

### Create Product

```http
POST /products
```

**Request Body:**
| Field | Type | Required | Example | Notes |
|-------|------|----------|---------|-------|
| sku | string | No | "SOAP002" | Auto-generated if not provided |
| name | string | Yes | "Lux White Soap 100g" | Maximum 255 characters |
| category | string | Yes | "Personal Care" | Grouping for reporting |
| cost_price_tzs | number | Yes | 1200 | Cost to acquire |
| selling_price_tzs | number | Yes | 1500 | Retail price |
| reorder_level | integer | No | 50 | Minimum stock threshold |
| description | string | No | "Premium soap..." | Product details |
| image_url | string | No | "https://..." | Product image link |
| is_active | boolean | No | true | Active status |

**Example Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Lux White Soap 100g",
    "category": "Personal Care",
    "cost_price_tzs": 1200,
    "selling_price_tzs": 1500,
    "reorder_level": 50,
    "description": "Premium white soap",
    "image_url": "https://via.placeholder.com/200"
  }'
```

**Success Response (201):**
```json
{
  "status": "success",
  "message": "Product created",
  "data": {
    "product_id": 11,
    "sku": "SKU-20260304133042-01",
    "name": "Lux White Soap 100g",
    ...
  }
}
```

**Error Response (400):**
```json
{
  "status": "error",
  "message": "Missing field: cost_price_tzs"
}
```

**Error Response (409):**
```json
{
  "status": "error",
  "message": "SKU already exists"
}
```

---

### Update Product

```http
PUT /products/{product_id}
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| product_id | integer | Product ID |

**Request Body:**
Any of the product fields (all optional):
```json
{
  "name": "Updated Name",
  "selling_price_tzs": 2000,
  "reorder_level": 60
}
```

**Example Request:**
```bash
curl -X PUT http://127.0.0.1:5000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{
    "selling_price_tzs": 1800,
    "description": "Updated description"
  }'
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Product updated",
  "data": {
    "product_id": 1,
    "selling_price_tzs": 1800,
    ...
  }
}
```

---

### Delete (Archive) Product

```http
DELETE /products/{product_id}
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| product_id | integer | Product ID |

**Note:** This is a soft-delete. The product is archived (is_active=false) but data is preserved.

**Example Request:**
```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/products/1
```

**Success Response (200):**
```json
{
  "status": "success",
  "message": "Product archived"
}
```

---

## Search & Filter

### Search Products

```http
GET /products/search
```

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| q | string | Yes | Search term (min 2 characters) |

**Searches in:** SKU, Name

**Example Request:**
```bash
GET /api/v1/products/search?q=soap
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "product_id": 1,
      "sku": "SOAP001",
      "name": "Lux White Soap 100g",
      ...
    },
    {
      "product_id": 2,
      "sku": "SOAP002",
      "name": "Omo Soap 100g",
      ...
    }
  ]
}
```

---

### Filter by Category

```http
GET /products/category/{category}
```

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| category | string | Category name |

**Example Request:**
```bash
GET /api/v1/products/category/Personal%20Care
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    { product object },
    { product object }
  ]
}
```

---

### Low Stock Products

```http
GET /products/low-stock
```

**Note:** Returns products that may need reordering (below reorder_level)

**Example Request:**
```bash
GET /api/v1/products/low-stock
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    {
      "product_id": 5,
      "sku": "SUGAR001",
      "reorder_level": 30,
      ...
    }
  ]
}
```

---

## Categories

### Get All Categories

```http
GET /categories
```

**Example Request:**
```bash
GET /api/v1/categories
```

**Success Response (200):**
```json
{
  "status": "success",
  "data": [
    "Personal Care",
    "Grains",
    "Cooking",
    "Spices",
    "Sweeteners",
    "Dairy",
    "Beverages",
    "Soft Drinks",
    "Home Care"
  ]
}
```

---

## Statistics

### Get Product Statistics

```http
GET /products/stats
```

**Returns:** Inventory value, margins, product counts

**Example Request:**
```bash
GET /api/v1/products/stats
```

**Success Response (200):**
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

**Field Descriptions:**
- `total_products` - All products (active + archived)
- `active_products` - Products available for sale
- `archived_products` - Deleted/inactive products
- `total_cost_value_tzs` - Sum of all cost prices
- `total_selling_value_tzs` - Sum of all selling prices
- `average_margin_percent` - Average profit margin across all products

---

## Error Handling

### Standard Error Response (4xx/5xx)

```json
{
  "status": "error",
  "message": "Error description"
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK - Request successful | GET, PUT |
| 201 | Created - New resource created | POST |
| 400 | Bad Request - Invalid input | Missing required field |
| 404 | Not Found - Resource doesn't exist | Invalid product_id |
| 409 | Conflict - Resource already exists | Duplicate SKU |
| 500 | Server Error - Unexpected error | Database connection failed |

---

## Examples

### Example 1: Add Product & Check Margin

```bash
# Create a new product
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rice - Pishori 2kg",
    "category": "Grains",
    "cost_price_tzs": 3500,
    "selling_price_tzs": 4200,
    "reorder_level": 30
  }'

# Response shows margin_percent: 20.0
```

### Example 2: Search for Products Starting with "l"

```bash
# Search
curl "http://127.0.0.1:5000/api/v1/products/search?q=l"

# Returns all products with names containing "l" (e.g., "Lux", "Oil", "Milk")
```

### Example 3: Get Products in Beverages Category

```bash
curl "http://127.0.0.1:5000/api/v1/products/category/Beverages"

# Returns: Coca Cola, Minute Maid, Tea
```

### Example 4: Monitor Inventory

```bash
# Get statistics
curl http://127.0.0.1:5000/api/v1/products/stats

# Response shows total inventory value, helps with cash flow planning
```

### Example 5: Update Pricing

```bash
# Increase price of product 5 from 8000 to 9000 TZS
curl -X PUT http://127.0.0.1:5000/api/v1/products/5 \
  -H "Content-Type: application/json" \
  -d '{
    "selling_price_tzs": 9000
  }'
```

---

## Testing with cURL

### Quick Test Script
```bash
#!/bin/bash
# Save as test-api.sh and run with: bash test-api.sh

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "1. Get all products..."
curl -s $BASE_URL/products | python -m json.tool | head -20

echo -e "\n2. Get categories..."
curl -s $BASE_URL/categories | python -m json.tool

echo -e "\n3. Get statistics..."
curl -s $BASE_URL/products/stats | python -m json.tool

echo -e "\n4. Search for 'soap'..."
curl -s "$BASE_URL/products/search?q=soap" | python -m json.tool

echo -e "\nAll tests completed!"
```

---

## Rate Limiting

Currently: No rate limiting (development mode)

**Planned for Phase 2:**
- 100 requests per minute per IP
- 1000 requests per day per user
- Proper error responses (429 Too Many Requests)

---

## Versioning

This is API v1. Future changes will use:
- `/api/v2/products` (when breaking changes occur)
- Backward compatibility maintained for v1

---

## Pagination Limits

- Minimum limit: 1
- Maximum limit: 100
- Default: 20 items per page

---

**Last Updated:** March 4, 2026  
**Status:** Production Ready (Phase 1)
