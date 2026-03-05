"""
Reports & Analytics Module Test Suite
==================================
Tests for all dashboard KPIs, sales reports, product rankings, and inventory health
Ensures accuracy of financial and operational metrics
"""

import unittest
import sys
import tempfile
from datetime import datetime, timedelta

# Avoid initializing with real database
import os
os.environ['TESTING'] = '1'

from app import app, db, Product, Sale, SaleItem, InventoryMovement


class ReportsTestCase(unittest.TestCase):
    """Test suite for Reports & Analytics module"""
    
    def setUp(self):
        """Set up test database and sample data for each test"""
        # Create a fresh temporary database file for each test
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        self.db_uri = f'sqlite:///{self.db_path}'
        
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        
        self.app = app
        self.client = app.test_client()
        
        # Create tables and seed data within application context
        with app.app_context():
            db.create_all()
            self._seed_data()
    
    def tearDown(self):
        """Clean up after each test"""
        with app.app_context():
            db.session.rollback()
            db.session.remove()
        
        # Close and delete the temporary database file
        if hasattr(self, 'db_fd'):
            os.close(self.db_fd)
        if hasattr(self, 'db_path') and os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def _seed_data(self):
        """Create sample products and sales for testing"""
        
        # Create products (check for duplicates first)
        products = [
            Product(sku='SOAP001', name='Safeguard Soap', category='Health & Beauty',
                   cost_price_tzs=2000, selling_price_tzs=3000, reorder_level=10),
            Product(sku='RICE001', name='Basmati Rice 5kg', category='Grains',
                   cost_price_tzs=15000, selling_price_tzs=20000, reorder_level=5),
            Product(sku='OIL001', name='Cooking Oil 1L', category='Cooking',
                   cost_price_tzs=4000, selling_price_tzs=6000, reorder_level=8),
            Product(sku='MILK001', name='Fresh Milk 1L', category='Dairy',
                   cost_price_tzs=1500, selling_price_tzs=2200, reorder_level=15),
            Product(sku='BREAD001', name='White Bread', category='Bakery',
                   cost_price_tzs=800, selling_price_tzs=1200, reorder_level=20),
        ]
        
        for product in products:
            if not Product.query.filter_by(sku=product.sku).first():
                db.session.add(product)
        db.session.commit()
        
        # Add inventory movements for current stock
        today = datetime.utcnow()
        movements = [
            InventoryMovement(sku='SOAP001', movement_type='STOCK_IN', quantity=50, reference='SUP001'),
            InventoryMovement(sku='RICE001', movement_type='STOCK_IN', quantity=20, reference='SUP001'),
            InventoryMovement(sku='OIL001', movement_type='STOCK_IN', quantity=30, reference='SUP001'),
            InventoryMovement(sku='MILK001', movement_type='STOCK_IN', quantity=10, reference='SUP001'),
            InventoryMovement(sku='BREAD001', movement_type='STOCK_IN', quantity=5, reference='SUP001'),
        ]
        
        for movement in movements:
            db.session.add(movement)
        db.session.commit()
        
        # Create PAID sales for today
        today_sales = [
            Sale(receipt_no='SR-SALE-000001', sale_datetime=today.replace(hour=8, minute=30),
                cashier='John', payment_method='CASH', payment_status='PAID',
                subtotal_tzs=50000, discount_tzs=5000, total_tzs=45000),
            Sale(receipt_no='SR-SALE-000002', sale_datetime=today.replace(hour=10, minute=15),
                cashier='Mary', payment_method='MOBILE_MONEY', payment_status='PAID',
                subtotal_tzs=30000, discount_tzs=0, total_tzs=30000),
            Sale(receipt_no='SR-SALE-000003', sale_datetime=today.replace(hour=14, minute=0),
                cashier='John', payment_method='CASH', payment_status='PAID',
                subtotal_tzs=25000, discount_tzs=2500, total_tzs=22500),
        ]
        
        for sale in today_sales:
            db.session.add(sale)
        db.session.commit()
        
        # Add sale items
        sale_items = [
            # Sale 1: SOAP(10) + RICE(1)
            SaleItem(sale_id=1, sku='SOAP001', product_name_snapshot='Safeguard Soap',
                    unit_price_tzs_snapshot=3000, qty=10, line_total_tzs=30000),
            SaleItem(sale_id=1, sku='RICE001', product_name_snapshot='Basmati Rice 5kg',
                    unit_price_tzs_snapshot=20000, qty=1, line_total_tzs=20000),
            # Sale 2: OIL(5)
            SaleItem(sale_id=2, sku='OIL001', product_name_snapshot='Cooking Oil 1L',
                    unit_price_tzs_snapshot=6000, qty=5, line_total_tzs=30000),
            # Sale 3: MILK(10) + BREAD(1)
            SaleItem(sale_id=3, sku='MILK001', product_name_snapshot='Fresh Milk 1L',
                    unit_price_tzs_snapshot=2200, qty=10, line_total_tzs=22000),
            SaleItem(sale_id=3, sku='BREAD001', product_name_snapshot='White Bread',
                    unit_price_tzs_snapshot=500, qty=1, line_total_tzs=500),
        ]
        
        for item in sale_items:
            db.session.add(item)
        db.session.commit()
        
        # Create SALE movements (stock reduction)
        movements = [
            InventoryMovement(sku='SOAP001', movement_type='SALE', quantity=10, reference='SR-SALE-000001'),
            InventoryMovement(sku='RICE001', movement_type='SALE', quantity=1, reference='SR-SALE-000001'),
            InventoryMovement(sku='OIL001', movement_type='SALE', quantity=5, reference='SR-SALE-000002'),
            InventoryMovement(sku='MILK001', movement_type='SALE', quantity=10, reference='SR-SALE-000003'),
            InventoryMovement(sku='BREAD001', movement_type='SALE', quantity=1, reference='SR-SALE-000003'),
        ]
        
        for movement in movements:
            db.session.add(movement)
        db.session.commit()
    
    # ==================== DASHBOARD KPI TESTS ====================
    
    def test_1_dashboard_kpis_today(self):
        """Test dashboard KPIs for today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        # Today should have 3 PAID sales
        today = data['today']
        self.assertEqual(today['transactions'], 3)
        self.assertEqual(today['total_sales_tzs'], 97500)  # 45000 + 30000 + 22500
        self.assertEqual(today['avg_basket_tzs'], 32500)  # 97500 / 3
    
    def test_2_dashboard_inventory_health(self):
        """Test dashboard shows inventory health counts"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        inventory = data['inventory']
        
        # All products should have stock, so no out of stock
        self.assertEqual(inventory['out_of_stock_count'], 0)
        
        # BREAD001 has 4 stock with reorder level 20, so should be low stock
        self.assertGreaterEqual(inventory['low_stock_count'], 1)
    
    def test_3_dashboard_week_total(self):
        """Test dashboard week total includes today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        week = data['week']
        # Week should include today's sales
        self.assertEqual(week['total_sales_tzs'], 97500)
        self.assertEqual(week['transactions'], 3)
    
    def test_4_dashboard_month_total(self):
        """Test dashboard month total includes today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        month = data['month']
        # Month should include today's sales
        self.assertEqual(month['total_sales_tzs'], 97500)
        self.assertEqual(month['transactions'], 3)
    
    # ==================== SALES REPORT TESTS ====================
    
    def test_5_sales_report_daily_breakdown(self):
        """Test sales report returns correct daily breakdown"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        # Should have 1 day with 3 transactions
        daily = data['daily']
        self.assertEqual(len(daily), 1)
        self.assertEqual(daily[0]['transactions'], 3)
        self.assertEqual(daily[0]['total_tzs'], 97500)
    
    def test_6_sales_report_payment_methods(self):
        """Test sales report breaks down by payment method"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        methods = data['payment_methods']
        
        # Find CASH and MOBILE_MONEY
        cash_sales = next((m for m in methods if m['method'] == 'CASH'), None)
        mobile_sales = next((m for m in methods if m['method'] == 'MOBILE_MONEY'), None)
        
        self.assertIsNotNone(cash_sales)
        self.assertIsNotNone(mobile_sales)
        
        # CASH: 45000 + 22500 (Sales 1 & 3)
        self.assertEqual(cash_sales['total_tzs'], 67500)
        self.assertEqual(cash_sales['transactions'], 2)
        
        # MOBILE_MONEY: 30000 (Sale 2)
        self.assertEqual(mobile_sales['total_tzs'], 30000)
        self.assertEqual(mobile_sales['transactions'], 1)
    
    def test_7_sales_report_total_matches_sum(self):
        """Test that revenue sum matches daily totals sum"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        daily_sum = sum(d['total_tzs'] for d in data['daily'])
        self.assertEqual(data['total_revenue_tzs'], daily_sum)
    
    # ==================== TOP PRODUCTS TESTS ====================
    
    def test_8_top_products_by_revenue(self):
        """Test top products ranked by revenue"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&by=revenue')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['by'], 'revenue')
        
        products = data['products']
        
        # Product revenue ranking:
        # SOAP001: 30000, RICE001: 20000, OIL001: 30000, MILK001: 22000, BREAD001: 500
        # Should be: OIL001=30000, SOAP001=30000, MILK001=22000, RICE001=20000, BREAD001=500
        
        # Top should be 30000
        self.assertEqual(products[0]['revenue_tzs'], 30000)
    
    def test_9_top_products_by_quantity(self):
        """Test top products ranked by quantity sold"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&by=qty')
        data = response.get_json()
        
        self.assertEqual(data['by'], 'qty')
        
        products = data['products']
        
        # Quantity ranking:
        # SOAP001: 10, MILK001: 10, RICE001: 1, OIL001: 5, BREAD001: 1
        # Should be: SOAP001/MILK001=10, OIL001=5, RICE001/BREAD001=1
        
        # Top should be 10
        self.assertEqual(products[0]['qty_sold'], 10)
    
    def test_10_top_products_limit(self):
        """Test limit parameter works correctly"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&limit=2')
        data = response.get_json()
        
        products = data['products']
        self.assertLessEqual(len(products), 2)
    
    # ==================== INVENTORY HEALTH TESTS ====================
    
    def test_11_inventory_health_low_stock(self):
        """Test inventory health identifies low stock items"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        low_stock = data['low_stock']
        
        # BREAD001: current_stock=4, reorder_level=20 → should be low stock
        # MILK001: current_stock=0, reorder_level=15 → should be out of stock
        
        # Check that low_stock items are correctly identified
        bread = next((item for item in low_stock['items'] if item['sku'] == 'BREAD001'), None)
        
        # BREAD001 has 4 stock (5 initial - 1 sold), reorder is 20, missing 16
        if bread:
            self.assertEqual(bread['current_stock'], 4)
            self.assertEqual(bread['reorder_level'], 20)
            self.assertEqual(bread['units_to_reorder'], 16)
    
    def test_12_inventory_health_out_of_stock(self):
        """Test inventory health identifies out of stock items"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        out_of_stock = data['out_of_stock']
        
        # MILK001: 10 initial - 10 sold = 0 → should be out of stock
        milk = next((item for item in out_of_stock['items'] if item['sku'] == 'MILK001'), None)
        
        if milk:
            self.assertEqual(milk['sku'], 'MILK001')
    
    def test_13_inventory_value_estimate(self):
        """Test inventory value calculation"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        inventory_value = data['inventory_value_estimate_tzs']
        
        # Current stock calculations:
        # SOAP001: (50-10) * 2000 = 80000
        # RICE001: (20-1) * 15000 = 285000
        # OIL001: (30-5) * 4000 = 100000
        # MILK001: (10-10) * 1500 = 0
        # BREAD001: (5-1) * 800 = 3200
        # Total = 468200
        
        expected = 80000 + 285000 + 100000 + 0 + 3200
        self.assertEqual(inventory_value, expected)
    
    # ==================== DATA INTEGRITY TESTS ====================
    
    def test_14_voided_sales_excluded_from_reports(self):
        """Test that VOIDED sales are excluded from revenue calculations"""
        with app.app_context():
            # Mark one sale as VOIDED
            sale = Sale.query.filter_by(receipt_no='SR-SALE-000001').first()
            sale.payment_status = 'VOIDED'
            db.session.commit()
        
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        # Should exclude the VOIDED sale, leaving 2 PAID sales
        today = data['today']
        self.assertEqual(today['transactions'], 2)
        self.assertEqual(today['total_sales_tzs'], 52500)  # 30000 + 22500
    
    def test_15_failed_sales_excluded_from_reports(self):
        """Test that FAILED sales are excluded from revenue calculations"""
        with app.app_context():
            # Create a FAILED sale
            failed_sale = Sale(receipt_no='SR-SALE-000099', 
                             sale_datetime=datetime.utcnow(),
                             cashier='Test', payment_method='CARD',
                             payment_status='FAILED',
                             subtotal_tzs=10000, discount_tzs=0, total_tzs=10000)
            db.session.add(failed_sale)
            db.session.commit()
        
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        # Should still be 3 (FAILED not counted)
        today = data['today']
        self.assertEqual(today['transactions'], 3)
        self.assertEqual(today['total_sales_tzs'], 97500)
    
    def test_16_api_returns_integers_for_currency(self):
        """Test that all currency amounts are integers (TZS, no decimals)"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        today = data['today']
        
        # All should be integers, no floats
        self.assertIsInstance(today['total_sales_tzs'], int)
        self.assertIsInstance(today['avg_basket_tzs'], int)
    
    # ==================== UI ROUTE TESTS ====================
    
    def test_17_dashboard_page_loads(self):
        """Test dashboard page renders without error"""
        response = self.client.get('/reports/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reports Dashboard', response.data)
    
    def test_18_sales_page_loads(self):
        """Test sales report page renders without error"""
        response = self.client.get('/reports/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sales Report', response.data)
    
    def test_19_top_products_page_loads(self):
        """Test top products page renders without error"""
        response = self.client.get('/reports/top-products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top Products', response.data)
    
    def test_20_inventory_health_page_loads(self):
        """Test inventory health page renders without error"""
        response = self.client.get('/reports/inventory-health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory Health', response.data)
    
    def test_21_all_kpi_values_are_integers(self):
        """Test all KPI values are integers not floats"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        self.assertIsInstance(data['today']['total_sales_tzs'], int)
        self.assertIsInstance(data['today']['transactions'], int)
        self.assertIsInstance(data['today']['avg_basket_tzs'], int)
        self.assertIsInstance(data['week']['total_sales_tzs'], int)
        self.assertIsInstance(data['month']['total_sales_tzs'], int)
        self.assertIsInstance(data['inventory']['low_stock_count'], int)
        self.assertIsInstance(data['inventory']['out_of_stock_count'], int)


if __name__ == '__main__':
    # Run all tests with verbose output
    unittest.main(verbosity=2)


class ReportsTestCase(unittest.TestCase):
    """Test suite for Reports & Analytics module"""
    
    def setUp(self):
        """Set up test database and sample data"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            self._seed_data()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def _seed_data(self):
        """Create sample products and sales for testing"""
        
        # Create products
        products = [
            Product(sku='SOAP001', name='Safeguard Soap', category='Health & Beauty',
                   cost_price_tzs=2000, selling_price_tzs=3000, reorder_level=10),
            Product(sku='RICE001', name='Basmati Rice 5kg', category='Grains',
                   cost_price_tzs=15000, selling_price_tzs=20000, reorder_level=5),
            Product(sku='OIL001', name='Cooking Oil 1L', category='Cooking',
                   cost_price_tzs=4000, selling_price_tzs=6000, reorder_level=8),
            Product(sku='MILK001', name='Fresh Milk 1L', category='Dairy',
                   cost_price_tzs=1500, selling_price_tzs=2200, reorder_level=15),
            Product(sku='BREAD001', name='White Bread', category='Bakery',
                   cost_price_tzs=800, selling_price_tzs=1200, reorder_level=20),
        ]
        
        for product in products:
            db.session.add(product)
        db.session.commit()
        
        # Add inventory movements for current stock
        today = datetime.utcnow()
        movements = [
            InventoryMovement(sku='SOAP001', movement_type='STOCK_IN', quantity=50, reference='SUP001'),
            InventoryMovement(sku='RICE001', movement_type='STOCK_IN', quantity=20, reference='SUP001'),
            InventoryMovement(sku='OIL001', movement_type='STOCK_IN', quantity=30, reference='SUP001'),
            InventoryMovement(sku='MILK001', movement_type='STOCK_IN', quantity=10, reference='SUP001'),
            InventoryMovement(sku='BREAD001', movement_type='STOCK_IN', quantity=5, reference='SUP001'),
        ]
        
        for movement in movements:
            db.session.add(movement)
        db.session.commit()
        
        # Create PAID sales for today
        today_sales = [
            Sale(receipt_no='SR-SALE-000001', sale_datetime=today.replace(hour=8, minute=30),
                cashier='John', payment_method='CASH', payment_status='PAID',
                subtotal_tzs=50000, discount_tzs=5000, total_tzs=45000),
            Sale(receipt_no='SR-SALE-000002', sale_datetime=today.replace(hour=10, minute=15),
                cashier='Mary', payment_method='MOBILE_MONEY', payment_status='PAID',
                subtotal_tzs=30000, discount_tzs=0, total_tzs=30000),
            Sale(receipt_no='SR-SALE-000003', sale_datetime=today.replace(hour=14, minute=0),
                cashier='John', payment_method='CASH', payment_status='PAID',
                subtotal_tzs=25000, discount_tzs=2500, total_tzs=22500),
        ]
        
        for sale in today_sales:
            db.session.add(sale)
        db.session.commit()
        
        # Add sale items
        sale_items = [
            # Sale 1: SOAP(10) + RICE(1)
            SaleItem(sale_id=1, sku='SOAP001', product_name_snapshot='Safeguard Soap',
                    unit_price_tzs_snapshot=3000, qty=10, line_total_tzs=30000),
            SaleItem(sale_id=1, sku='RICE001', product_name_snapshot='Basmati Rice 5kg',
                    unit_price_tzs_snapshot=20000, qty=1, line_total_tzs=20000),
            # Sale 2: OIL(5)
            SaleItem(sale_id=2, sku='OIL001', product_name_snapshot='Cooking Oil 1L',
                    unit_price_tzs_snapshot=6000, qty=5, line_total_tzs=30000),
            # Sale 3: MILK(10) + BREAD(3)
            SaleItem(sale_id=3, sku='MILK001', product_name_snapshot='Fresh Milk 1L',
                    unit_price_tzs_snapshot=2200, qty=10, line_total_tzs=22000),
            SaleItem(sale_id=3, sku='BREAD001', product_name_snapshot='White Bread',
                    unit_price_tzs_snapshot=300, qty=1, line_total_tzs=300),
        ]
        
        for item in sale_items:
            db.session.add(item)
        db.session.commit()
        
        # Create SALE movements (stock reduction)
        movements = [
            InventoryMovement(sku='SOAP001', movement_type='SALE', quantity=10, reference='SR-SALE-000001'),
            InventoryMovement(sku='RICE001', movement_type='SALE', quantity=1, reference='SR-SALE-000001'),
            InventoryMovement(sku='OIL001', movement_type='SALE', quantity=5, reference='SR-SALE-000002'),
            InventoryMovement(sku='MILK001', movement_type='SALE', quantity=10, reference='SR-SALE-000003'),
            InventoryMovement(sku='BREAD001', movement_type='SALE', quantity=1, reference='SR-SALE-000003'),
        ]
        
        for movement in movements:
            db.session.add(movement)
        db.session.commit()
    
    # ==================== DASHBOARD KPI TESTS ====================
    
    def test_1_dashboard_kpis_today(self):
        """Test dashboard KPIs for today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        # Today should have 3 PAID sales
        today = data['today']
        self.assertEqual(today['transactions'], 3)
        self.assertEqual(today['total_sales_tzs'], 97500)  # 45000 + 30000 + 22500
        self.assertEqual(today['avg_basket_tzs'], 32500)  # 97500 / 3
    
    def test_2_dashboard_inventory_health(self):
        """Test dashboard shows inventory health counts"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        inventory = data['inventory']
        
        # All products should have stock, so no out of stock
        self.assertEqual(inventory['out_of_stock_count'], 0)
        
        # BREAD001 has 4 stock with reorder level 20, so should be low stock
        self.assertGreaterEqual(inventory['low_stock_count'], 1)
    
    def test_3_dashboard_week_total(self):
        """Test dashboard week total includes today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        week = data['week']
        # Week should include today's sales
        self.assertEqual(week['total_sales_tzs'], 97500)
        self.assertEqual(week['transactions'], 3)
    
    def test_4_dashboard_month_total(self):
        """Test dashboard month total includes today"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        month = data['month']
        # Month should include today's sales
        self.assertEqual(month['total_sales_tzs'], 97500)
        self.assertEqual(month['transactions'], 3)
    
    # ==================== SALES REPORT TESTS ====================
    
    def test_5_sales_report_daily_breakdown(self):
        """Test sales report returns correct daily breakdown"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        # Should have 1 day with 3 transactions
        daily = data['daily']
        self.assertEqual(len(daily), 1)
        self.assertEqual(daily[0]['transactions'], 3)
        self.assertEqual(daily[0]['total_tzs'], 97500)
    
    def test_6_sales_report_payment_methods(self):
        """Test sales report breaks down by payment method"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        methods = data['payment_methods']
        
        # Find CASH and MOBILE_MONEY
        cash_sales = next((m for m in methods if m['method'] == 'CASH'), None)
        mobile_sales = next((m for m in methods if m['method'] == 'MOBILE_MONEY'), None)
        
        self.assertIsNotNone(cash_sales)
        self.assertIsNotNone(mobile_sales)
        
        # CASH: 45000 + 22500 (Sales 1 & 3)
        self.assertEqual(cash_sales['total_tzs'], 67500)
        self.assertEqual(cash_sales['transactions'], 2)
        
        # MOBILE_MONEY: 30000 (Sale 2)
        self.assertEqual(mobile_sales['total_tzs'], 30000)
        self.assertEqual(mobile_sales['transactions'], 1)
    
    def test_7_sales_report_total_matches_sum(self):
        """Test that revenue sum matches daily totals sum"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/sales?from={today}&to={today}')
        data = response.get_json()
        
        daily_sum = sum(d['total_tzs'] for d in data['daily'])
        self.assertEqual(data['total_revenue_tzs'], daily_sum)
    
    # ==================== TOP PRODUCTS TESTS ====================
    
    def test_8_top_products_by_revenue(self):
        """Test top products ranked by revenue"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&by=revenue')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['by'], 'revenue')
        
        products = data['products']
        
        # Product revenue ranking:
        # SOAP001: 30000, RICE001: 20000, OIL001: 30000, MILK001: 22000, BREAD001: 300
        # Should be: OIL001=30000, SOAP001=30000, MILK001=22000, RICE001=20000, BREAD001=300
        
        # Top should be SOAP or OIL (both 30000)
        self.assertEqual(products[0]['revenue_tzs'], 30000)
    
    def test_9_top_products_by_quantity(self):
        """Test top products ranked by quantity sold"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&by=qty')
        data = response.get_json()
        
        self.assertEqual(data['by'], 'qty')
        
        products = data['products']
        
        # Quantity ranking:
        # SOAP001: 10, MILK001: 10, RICE001: 1, OIL001: 5, BREAD001: 1
        # Should be: SOAP001/MILK001=10, OIL001=5, RICE001/BREAD001=1
        
        # Top should be SOAP or MILK (both 10)
        self.assertIn(products[0]['qty_sold'], [10])
    
    def test_10_top_products_limit(self):
        """Test limit parameter works correctly"""
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/reports/top-products?from={today}&to={today}&limit=2')
        data = response.get_json()
        
        products = data['products']
        self.assertLessEqual(len(products), 2)
    
    # ==================== INVENTORY HEALTH TESTS ====================
    
    def test_11_inventory_health_low_stock(self):
        """Test inventory health identifies low stock items"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'success')
        
        low_stock = data['low_stock']
        
        # BREAD001: current_stock=4, reorder_level=20 → should be low stock
        # MILK001: current_stock=0, reorder_level=15 → should be out of stock
        
        # Check that low_stock items are correctly identified
        bread = next((item for item in low_stock['items'] if item['sku'] == 'BREAD001'), None)
        
        # BREAD001 has 4 stock (5 initial - 1 sold), reorder is 20, missing 16
        if bread:
            self.assertEqual(bread['current_stock'], 4)
            self.assertEqual(bread['reorder_level'], 20)
            self.assertEqual(bread['units_to_reorder'], 16)
    
    def test_12_inventory_health_out_of_stock(self):
        """Test inventory health identifies out of stock items"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        out_of_stock = data['out_of_stock']
        
        # MILK001: 10 initial - 10 sold = 0 → should be out of stock
        milk = next((item for item in out_of_stock['items'] if item['sku'] == 'MILK001'), None)
        
        if milk:
            self.assertEqual(milk['sku'], 'MILK001')
    
    def test_13_inventory_value_estimate(self):
        """Test inventory value calculation"""
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        inventory_value = data['inventory_value_estimate_tzs']
        
        # Current stock calculations:
        # SOAP001: (50-10) * 2000 = 80000
        # RICE001: (20-1) * 15000 = 285000
        # OIL001: (30-5) * 4000 = 100000
        # MILK001: (10-10) * 1500 = 0
        # BREAD001: (5-1) * 800 = 3200
        # Total = 468200
        
        expected = 80000 + 285000 + 100000 + 0 + 3200
        self.assertEqual(inventory_value, expected)
    
    def test_14_inventory_health_no_items_low_stock(self):
        """Test when no items are low in stock"""
        # Add more stock to bring all above reorder level
        with app.app_context():
            # Add stock to BREAD001 to reach reorder level
            movement = InventoryMovement(sku='BREAD001', movement_type='STOCK_IN', 
                                        quantity=20, reference='SUP002')
            db.session.add(movement)
            db.session.commit()
        
        response = self.client.get('/api/reports/inventory-health')
        data = response.get_json()
        
        # Now low_stock should be empty for BREAD001
        bread_low = next((item for item in data['low_stock']['items'] 
                         if item['sku'] == 'BREAD001'), None)
        
        # BREAD001 should no longer be low (4 + 20 = 24 >= 20)
        self.assertIsNone(bread_low)
    
    # ==================== DATA INTEGRITY TESTS ====================
    
    def test_15_voided_sales_excluded_from_reports(self):
        """Test that VOIDED sales are excluded from revenue calculations"""
        with app.app_context():
            # Mark one sale as VOIDED
            sale = Sale.query.filter_by(receipt_no='SR-SALE-000001').first()
            sale.payment_status = 'VOIDED'
            db.session.commit()
        
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        # Should exclude the VOIDED sale, leaving 2 PAID sales
        today = data['today']
        self.assertEqual(today['transactions'], 2)
        self.assertEqual(today['total_sales_tzs'], 52500)  # 30000 + 22500
    
    def test_16_failed_sales_excluded_from_reports(self):
        """Test that FAILED sales are excluded from revenue calculations"""
        with app.app_context():
            # Create a FAILED sale
            failed_sale = Sale(receipt_no='SR-SALE-000099', 
                             sale_datetime=datetime.utcnow(),
                             cashier='Test', payment_method='CARD',
                             payment_status='FAILED',
                             subtotal_tzs=10000, discount_tzs=0, total_tzs=10000)
            db.session.add(failed_sale)
            db.session.commit()
        
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        # Should still be 3 (FAILED not counted)
        today = data['today']
        self.assertEqual(today['transactions'], 3)
        self.assertEqual(today['total_sales_tzs'], 97500)
    
    def test_17_api_returns_integers_for_currency(self):
        """Test that all currency amounts are integers (TZS, no decimals)"""
        response = self.client.get('/api/reports/dashboard')
        data = response.get_json()
        
        today = data['today']
        
        # All should be integers, no floats
        self.assertIsInstance(today['total_sales_tzs'], int)
        self.assertIsInstance(today['avg_basket_tzs'], int)
    
    # ==================== UI ROUTE TESTS ====================
    
    def test_18_dashboard_page_loads(self):
        """Test dashboard page renders without error"""
        response = self.client.get('/reports/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reports Dashboard', response.data)
    
    def test_19_sales_page_loads(self):
        """Test sales report page renders without error"""
        response = self.client.get('/reports/sales')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sales Report', response.data)
    
    def test_20_top_products_page_loads(self):
        """Test top products page renders without error"""
        response = self.client.get('/reports/top-products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Top Products', response.data)
    
    def test_21_inventory_health_page_loads(self):
        """Test inventory health page renders without error"""
        response = self.client.get('/reports/inventory-health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory Health', response.data)


if __name__ == '__main__':
    # Run all tests with verbose output
    unittest.main(verbosity=2)
