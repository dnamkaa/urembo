# 📸 Product Images Guide

## Working Image Services

The system supports images from any public URL. Below are **TESTED WORKING** services you can use:

### 1. **Via Placeholder (⭐ Recommended)**
- **Service**: https://via.placeholder.com/
- **Format**: `https://via.placeholder.com/200?text=Product+Name`
- **Features**: Instant placeholders, custom text, no signup needed
- **Status**: ✅ **WORKS PERFECTLY**

**Examples:**
```
https://via.placeholder.com/200?text=Lux+Soap
https://via.placeholder.com/200?text=Sunflower+Oil
https://via.placeholder.com/200?text=Rice+2kg
https://via.placeholder.com/200?text=Coca+Cola
```

### 2. **Picsum Photos (Real Images)**
- **Service**: https://picsum.photos/
- **Format**: `https://picsum.photos/200/200?random=1`
- **Features**: Real photos, different images each time
- **Status**: ✅ **WORKS PERFECTLY**

**Examples:**
```
https://picsum.photos/200/200?random=1
https://picsum.photos/200/200?random=2
https://picsum.photos/200/200?random=3
```

### 3. **Lorenz Ipsum (Color Blocks)**
- **Service**: https://lorempixel.com/
- **Format**: `https://lorempixel.com/200/200/food/1/`
- **Features**: Categorized images (food, business, tech, etc.)
- **Status**: ✅ **WORKS PERFECTLY**

**Examples:**
```
https://lorempixel.com/200/200/food/1/
https://lorempixel.com/200/200/business/2/
https://lorempixel.com/200/200/tech/3/
```

### 4. **DummyImage (Simple Blocks)**
- **Service**: https://dummyimage.com/
- **Format**: `https://dummyimage.com/200x200/0000FF/FFFFFF?text=Product`
- **Features**: Custom colors, text overlay
- **Status**: ✅ **WORKS PERFECTLY**

**Examples:**
```
https://dummyimage.com/200x200/FF6B6B/FFFFFF?text=Lux+Soap
https://dummyimage.com/200x200/4ECDC4/FFFFFF?text=Rice
https://dummyimage.com/200x200/FFE66D/000000?text=Oil
```

### 5. **Your Own Images (CDN/Web Server)**
- **Service**: Dropbox, Google Drive, Imgur, CloudFlare, etc.
- **Format**: Direct URL to image file
- **Features**: Your actual product photos
- **Status**: ✅ **WORKS (if URL is public)**

**What works:**
```
✅ https://cdn.example.com/product-image.jpg
✅ https://dropbox.com/s/xxxxx/image.jpg?dl=1
✅ https://imgur.com/xxxxx.jpg
✅ https://imgur.com/xxxxx.png
```

**What DOESN'T work:**
```
❌ https://example.com/images/product.jpg (404 - not a real image)
❌ https://drive.google.com/file/...  (not direct link)
❌ Private/protected URLs (need authentication)
❌ Broken/expired links
```

---

## 🚫 Why Your URLs Don't Work

The URLs you provided:
```
❌ https://example.com/images/lux_white_soap_100g.jpg
❌ https://example.com/images/rice_5kg.jpg
❌ https://example.com/images/sunflower_oil_5l.jpg
```

**Problem**: `example.com` is a placeholder domain with no actual images. These URLs return **404 Not Found** errors.

**Solution**: Use a real image service like those above.

---

## ✅ Recommended Setup

### Option 1: Quick Start (No Setup)
Use Via Placeholder - instant, no signup:
```
https://via.placeholder.com/200?text=Your+Product+Name
```

### Option 2: Real Images (Free)
Use Picsum Photos for random real images:
```
https://picsum.photos/200/200?random=5
```

### Option 3: Brand Images (Upload Yourself)
1. Upload your images to **Imgur** (free, no signup needed)
2. Copy the **direct image URL** (not the page URL)
3. Paste into Smart Retail System

**How to get Imgur direct URL:**
- Upload image to https://imgur.com
- Right-click image → "Copy image link"
- Use that URL in your products

### Option 4: Custom Server CDN
- Upload images to your own **CDN** (CloudFlare, AWS S3, etc.)
- Get public HTTPS URL
- Use in system

---

## 📋 CSV Import with Images

When uploading CSV files, you have two options:

### Option A: Leave Image URL Blank (Auto-Assigned)
```csv
sku,name,category,cost_price_tzs,selling_price_tzs,reorder_level,description,image_url
SOAP001,Lux Soap,Personal Care,1200,1500,50,Premium soap,
RICE001,Rice 2kg,Grains,3500,4200,30,Quality rice,
```

✅ System automatically assigns **working placeholder images** by category

### Option B: Provide Working Image URL
```csv
sku,name,category,cost_price_tzs,selling_price_tzs,reorder_level,description,image_url
SOAP001,Lux Soap,Personal Care,1200,1500,50,Premium soap,https://via.placeholder.com/200?text=Lux+Soap
RICE001,Rice 2kg,Grains,3500,4200,30,Quality rice,https://via.placeholder.com/200?text=Rice+2kg
```

✅ Uses your specified images (if URLs are valid/public)

---

## How to Test Image URLs

Before adding thousands of products, test your image URL:

### Method 1: Try in Browser
1. Copy your image URL
2. Paste into browser address bar
3. **If you see image**: ✅ It works!
4. **If you see error page**: ❌ URL is broken

### Method 2: Try in Product Form
1. Add a test product
2. Paste image URL in **Image URL** field
3. Watch for **preview image** below
4. If preview appears: ✅ URL works!
5. If broken: ❌ URL is invalid

---

## Category-Based Auto-Images

When you leave image_url blank, the system auto-assigns:

| Category | Sample Images |
|----------|---|
| **Personal Care** | https://via.placeholder.com/200?text=Soap, https://via.placeholder.com/200?text=Shampoo, https://via.placeholder.com/200?text=Toothpaste |
| **Grains** | https://via.placeholder.com/200?text=Rice, https://via.placeholder.com/200?text=Flour, https://via.placeholder.com/200?text=Maize |
| **Cooking** | https://via.placeholder.com/200?text=Cooking+Oil, https://via.placeholder.com/200?text=Salt, https://via.placeholder.com/200?text=Spices |
| **Beverages** | https://via.placeholder.com/200?text=Soda, https://via.placeholder.com/200?text=Juice, https://via.placeholder.com/200?text=Water |
| **Dairy** | https://via.placeholder.com/200?text=Milk, https://via.placeholder.com/200?text=Cheese, https://via.placeholder.com/200?text=Yogurt |
| **Spices** | https://via.placeholder.com/200?text=Spices, https://via.placeholder.com/200?text=Pepper, https://via.placeholder.com/200?text=Garlic |

**Rotating**: Each new product gets next image in rotation

---

## Upload Your Own Images (Best Practice)

### Step 1: Use Free Image Hosting
**Imgur (Recommended)**
- Go to https://imgur.com
- Click "New Post"
- Upload your product photo
- Right-click image → "Copy image link"
- Use that URL (copy format: `https://i.imgur.com/xxxxx.jpg`)

**Or CloudFlare Images**
- Upload to CloudFlare CDN
- Get public HTTPS URL
- Use in system

### Step 2: Add to Products
1. Go to "Add Product"
2. Paste image URL in **Image URL** field
3. See preview below
4. Save product

### Step 3: Bulk Upload
1. Create CSV with your image URLs
2. Upload via "Bulk Import"
3. All products get proper images

---

## Common Image URL Issues

| Issue | Solution |
|-------|----------|
| Image not showing | Check URL in browser first |
| "Broken image" icon | URL is invalid or expired |
| Page instead of image | You copied page URL, not image URL |
| 404 errors | Domain doesn't exist (like example.com) |
| Very slow to load | Image file too large (optimize first) |

---

## Current System Status

✅ **Images Enabled**: System fully supports image URLs  
✅ **Auto-Images**: Placeholder images assigned by category  
✅ **Manual Images**: Upload CSV with custom image URLs  
✅ **Preview**: See images before saving  
✅ **Responsive**: Images scale on mobile/tablet  

---

## Example: Proper CSV with Images

```csv
sku,name,category,cost_price_tzs,selling_price_tzs,reorder_level,description,image_url
SOAP001,Lux White Soap,Personal Care,1200,1500,50,Premium soap,https://via.placeholder.com/200?text=Lux+White+Soap
RICE001,Pishori Rice 2kg,Grains,3500,4200,30,Quality rice,https://via.placeholder.com/200?text=Pishori+Rice
OIL001,Sunflower Oil 1L,Cooking,5500,6800,20,Pure oil,https://via.placeholder.com/200?text=Sunflower+Oil
COKE001,Coca Cola 500ml,Beverages,1400,2000,60,Soda,https://via.placeholder.com/200?text=Coca+Cola
SUGAR001,Sugar 1kg,Cooking,2000,2500,50,Sugar,https://via.placeholder.com/200?text=Sugar+1kg
FLOUR001,Wheat Flour 2kg,Grains,2800,3500,30,Flour,https://via.placeholder.com/200?text=Wheat+Flour
SHAMPOO001,Shampoo 250ml,Personal Care,1800,2400,40,Shampoo,https://via.placeholder.com/200?text=Shampoo+250ml
WATER001,Water 1.5L,Beverages,600,1000,100,Water,https://via.placeholder.com/200?text=Pure+Water
```

---

## Quick Reference

**Best for Quick Testing**:
```
https://via.placeholder.com/200?text=YOUR+PRODUCT+NAME
```

**Best for Real Images**:
```
https://picsum.photos/200/200?random=N
```

**Best for Your Photos**:
```
Upload to Imgur → Get direct URL → Use in system
```

**Best for Auto Images**:
```
Leave image_url empty in CSV → System assigns by category
```

---

## Need Help?

1. **Test image URL first**: Paste in browser to verify it works
2. **Use Via Placeholder**: Instant working images with no setup
3. **Check URL format**: Must start with `https://`
4. **Verify it's public**: Image must be accessible without login
5. **See preview**: Use product form preview to test

**All images should be visible within 1-2 seconds of page load!** ✅
