# Bulk Import Feature Guide

## Overview
The Smart Retail System now supports bulk importing products from CSV and Excel files with automatic sample images and SKU generation.

## Features

✅ **CSV Support** - Import from spreadsheets  
✅ **Excel Support** - XLSX and XLS formats  
✅ **Auto Images** - Products automatically get sample images by category  
✅ **Auto SKU** - Missing SKUs are generated automatically  
✅ **Validation** - All required fields are checked  
✅ **Duplicate Detection** - Existing SKUs are not re-imported  
✅ **Error Reporting** - Detailed feedback on each row  

## File Format

### Required Fields
```
sku, name, category, cost_price_tzs, selling_price_tzs, reorder_level, description, image_url
```

### Field Descriptions

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `sku` | Text | Optional | Auto-generated if empty (SKU-YYYYMMDDHHMMSS-XX) |
| `name` | Text | Yes | Product name (max 255 chars) |
| `category` | Text | Yes | Category name (e.g., "Personal Care") |
| `cost_price_tzs` | Number | Yes | Cost price in TZS (no commas) |
| `selling_price_tzs` | Number | Yes | Selling price in TZS (no commas) |
| `reorder_level` | Number | Optional | Minimum stock (default: 10) |
| `description` | Text | Optional | Product details |
| `image_url` | Text | Optional | Image link (auto-assigned if empty) |

## Sample CSV Format

```csv
sku,name,category,cost_price_tzs,selling_price_tzs,reorder_level,description,image_url
SOAP001,Lux White Soap 100g,Personal Care,1200,1500,50,Premium white soap,
RICE001,Pishori Rice 2kg,Grains,3500,4200,30,Premium rice,
OIL001,Sunflower Oil 1L,Cooking,5500,6800,20,Pure oil,
```

## How to Use

### Step 1: Navigate to Bulk Import
- Go to **Products** page
- Click **"Bulk Import"** button

### Step 2: Download Template (Optional)
- Click **"Download CSV Template"** to get a starter file
- Fill it with your product data

### Step 3: Upload File
- Click **"Select File"** and choose your CSV or XLSX
- Click **"Import Products"**

### Step 4: Review Results
- See import summary: X products imported, Y skipped
- Check any error messages for issues
- Refresh the products list to see new items

## Supported Categories

The system recognizes these category types for auto-image assignment:

- **Personal Care** - Soaps, shampoos, toothpaste, lotions
- **Grains** - Rice, flour, maize, beans, lentils
- **Cooking** - Oils, salt, vinegar, seasonings
- **Spices** - Pepper, garlic, turmeric, cinnamon
- **Beverages** - Soda, juice, water, tea, coffee
- **Dairy** - Milk, cheese, yogurt, butter

## Sample Data

A complete sample file with 50+ Tanzanian products is included in:
```
sample_imports/products_sample.csv
```

You can upload this directly to test the bulk import feature!

## Error Handling

### Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Missing fields: name | Product name not provided | Check CSV has 'name' column and value |
| Missing fields: category | No category specified | Add valid category from list above |
| Invalid data: cost_price_tzs | Cost price not a number | Use numbers only (e.g., 1200) |
| SKU already exists | Duplicate product | Use unique SKU or leave blank for auto-gen |
| Invalid file type | Wrong format uploaded | Use CSV, XLSX, or XLS only |

## Excel Spreadsheet Example

| sku | name | category | cost_price_tzs | selling_price_tzs | reorder_level | description | image_url |
|-----|------|----------|--------|----------|--------|-------------|-----------|
| SOAP001 | Lux Soap 100g | Personal Care | 1200 | 1500 | 50 | Premium soap | |
| RICE001 | Pishori Rice 2kg | Grains | 3500 | 4200 | 30 | Quality rice | |
| OIL001 | Sunflower Oil 1L | Cooking | 5500 | 6800 | 20 | Pure oil | |

## Tips & Best Practices

1. **Use Auto-Generation** - Leave SKU blank to auto-generate (safer than manual)
2. **Consistent Categories** - Use exact category names from the supported list
3. **TZS Only** - All prices must be in Tanzania Shillings
4. **Price Validation** - Ensure selling_price_tzs > cost_price_tzs
5. **Image URLs** - Leave blank for automatic sample images (recommended)
6. **Test First** - Start with 5-10 products before importing 100+
7. **Backup** - Keep a copy of your CSV/Excel locally

## Using Sample Images

The system automatically assigns product images by category:

- **Personal Care** → 3 soap/toiletry images
- **Grains** → 3 food item images
- **Cooking** → 3 cooking ingredient images
- **And more...** - Each category has 3 rotating images

**No action needed!** Just leave `image_url` column empty.

## Batch Processing Tips

### For Large Uploads (500+ products)

1. **Split into chunks** - Import 100-200 products at a time
2. **Verify each batch** - Check products list after each import
3. **Monitor errors** - Fix issues before next batch
4. **Document changes** - Keep track of imports for audit trail

### Performance

- **< 50 products** - Instant import (< 1 second)
- **50-200 products** - Quick import (1-3 seconds)
- **200-500 products** - Normal import (5-10 seconds)
- **500+ products** - Split into batches recommend

## API Integration

You can also import products via the API:

```bash
curl -X POST http://127.0.0.1:5000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "PROD001",
    "name": "Sample Product",
    "category": "Personal Care",
    "cost_price_tzs": 1000,
    "selling_price_tzs": 1500,
    "reorder_level": 10,
    "description": "Sample",
    "image_url": ""
  }'
```

## Troubleshooting

### "File won't upload"
- Check file size (max 16MB)
- Verify file format (CSV, XLSX, or XLS)
- Ensure no special characters in filename

### "Products imported but images missing"
- This is normal if you left `image_url` blank
- System uses auto-categories sample images
- Images update automatically in UI

### "Some products skipped"
- Check error messages for specific rows
- Verify all required fields are present
- Ensure SKUs are unique across imports

## Next Steps

1. **Download Template** `http://127.0.0.1:5000/products/bulk/template`
2. **Fill with Data** - Use Excel or Google Sheets
3. **Upload** - Via Products > Bulk Import button
4. **Verify** - Check products list for new items
5. **Customize** - Edit any product via form if needed

---

**Questions?** Check the system documentation or try the sample data first!
