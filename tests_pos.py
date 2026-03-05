"""
POS Sales Module Tests
Verifies all POS functionality and business logic
"""

import unittest
import json
from datetime import datetime
from app import app, db, Product, Sale, SaleItem, InventoryMovement


class POSSalesTests(unittest.TestCase):
    """Test suite for POS Sales Module"""
    
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.app = app
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Create test products
            prod1 = Product(
                sku='TEST001',
                name='Test Product 1',
                category='Test',
                cost_price_tzs=1000,
                selling_price_tzs=1500,
                reorder_level=5,
                is_active=True
            )
            prod2 = Product(
                sku='TEST002',
                name='Test Product 2',
                category='Test',
                cost_price_tzs=2000,
                selling_price_tzs=3000,
                reorder_level=10,
                is_active=True
            )
            
            db.session.add(prod1)
            db.session.add(prod2)
            db.session.flush()
            
            # Add initial stock via inventory movements
            mov1 = InventoryMovement(
                sku='TEST001',
                movement_type='STOCK_IN',
                quantity=50,
                reference='INIT001'
            )
            mov2 = InventoryMovement(
                sku='TEST002',
                movement_type='STOCK_IN',
                quantity=30,
                reference='INIT002'
            )
            
            db.session.add(mov1)
            db.session.add(mov2)
            db.session.commit()
    
    def tearDown(self):
        """Clean up after tests"""
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_1_product_search_api(self):
        """Test GET /api/pos/products returns products with stock info"""
        response = self.client.get('/api/pos/products')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']), 2)
        
        # Check first product
        prod = data['data'][0]
        self.assertEqual(prod['sku'], 'TEST001')
        self.assertEqual(prod['name'], 'Test Product 1')
        self.assertEqual(prod['selling_price_tzs'], 1500)
        self.assertEqual(prod['current_stock'], 50)
        self.assertTrue(prod['is_in_stock'])
    
    def test_2_product_search_by_sku(self):
        """Test product search filtering by SKU"""
        response = self.client.get('/api/pos/products?q=TEST001')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['sku'], 'TEST001')
    
    def test_3_product_search_by_name(self):
        """Test product search filtering by name"""
        response = self.client.get('/api/pos/products?q=Product%202')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['sku'], 'TEST002')
    
    def test_4_checkout_creates_sale(self):
        """Test POST /api/pos/sales creates sale header and items"""
        payload = {
            'cashier': 'John Doe',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 2},
                {'sku': 'TEST002', 'qty': 1}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('SR-SALE-', data['receipt_no'])
        self.assertEqual(data['sale_id'], 1)
        
        # Verify sale in database
        with app.app_context():
            sale = Sale.query.get(1)
            self.assertIsNotNone(sale)
            self.assertEqual(sale.cashier, 'John Doe')
            self.assertEqual(sale.payment_method, 'CASH')
            self.assertEqual(len(sale.items), 2)
            
            # Check totals
            # TEST001: 2 * 1500 = 3000
            # TEST002: 1 * 3000 = 3000
            # Total: 6000
            self.assertEqual(sale.subtotal_tzs, 6000)
            self.assertEqual(sale.total_tzs, 6000)
    
    def test_5_checkout_reduces_stock(self):
        """Test that checkout creates SALE movements and reduces stock"""
        payload = {
            'cashier': 'Jane Smith',
            'payment_method': 'MOBILE_MONEY',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 5}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        with app.app_context():
            # Check inventory movement created
            movements = InventoryMovement.query.filter_by(
                sku='TEST001',
                movement_type='SALE'
            ).all()
            self.assertEqual(len(movements), 1)
            self.assertEqual(movements[0].quantity, 5)
            
            # Check stock reduced
            product = Product.query.filter_by(sku='TEST001').first()
            current_stock = product.get_current_stock()
            self.assertEqual(current_stock, 45)  # 50 - 5
    
    def test_6_checkout_insufficient_stock(self):
        """Test that checkout fails if insufficient stock"""
        payload = {
            'cashier': 'Bob',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 100}  # Only 50 available
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'error')
        self.assertIn('Insufficient stock', data['message'])
    
    def test_7_checkout_with_discount(self):
        """Test checkout with discount applied"""
        payload = {
            'cashier': 'Alice',
            'payment_method': 'CARD',
            'discount_tzs': 1000,
            'items': [
                {'sku': 'TEST001', 'qty': 2}  # 2 * 1500 = 3000
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        
        with app.app_context():
            sale = Sale.query.get(data['sale_id'])
            self.assertEqual(sale.subtotal_tzs, 3000)
            self.assertEqual(sale.discount_tzs, 1000)
            self.assertEqual(sale.total_tzs, 2000)
    
    def test_8_receipt_number_increments(self):
        """Test that receipt numbers increment correctly"""
        with app.app_context():
            # Create first sale
            sale1 = Sale(
                receipt_no='SR-SALE-000001',
                cashier='User1',
                payment_method='CASH',
                payment_status='PAID',
                subtotal_tzs=5000,
                discount_tzs=0,
                total_tzs=5000
            )
            db.session.add(sale1)
            db.session.flush()
            
            # Create another sale
            payload = {
                'cashier': 'User2',
                'payment_method': 'MOBILE_MONEY',
                'discount_tzs': 0,
                'items': [
                    {'sku': 'TEST002', 'qty': 1}
                ]
            }
            
            response = self.client.post(
                '/api/pos/sales',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            data = json.loads(response.data)
            # Receipt should be SR-SALE-000002
            self.assertIn('000002', data['receipt_no'])
    
    def test_9_sale_items_snapshot_price(self):
        """Test that sale items store snapshot of price at time of sale"""
        payload = {
            'cashier': 'Charlie',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 3}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        with app.app_context():
            sale = Sale.query.get(1)
            item = sale.items[0]
            
            # Check snapshot stored correctly
            self.assertEqual(item.sku, 'TEST001')
            self.assertEqual(item.product_name_snapshot, 'Test Product 1')
            self.assertEqual(item.unit_price_tzs_snapshot, 1500)
            self.assertEqual(item.qty, 3)
            self.assertEqual(item.line_total_tzs, 4500)
    
    def test_10_sale_detail_api(self):
        """Test GET /api/pos/sales/{sale_id} returns full sale details"""
        # Create a sale first
        payload = {
            'cashier': 'David',
            'payment_method': 'BANK_TRANSFER',
            'discount_tzs': 500,
            'items': [
                {'sku': 'TEST001', 'qty': 2},
                {'sku': 'TEST002', 'qty': 1}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        sale_id = json.loads(response.data)['sale_id']
        
        # Get sale details
        response = self.client.get(f'/api/pos/sales/{sale_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        sale = data['data']
        self.assertEqual(sale['sale_id'], sale_id)
        self.assertEqual(sale['cashier'], 'David')
        self.assertEqual(len(sale['items']), 2)
        self.assertEqual(sale['discount_tzs'], 500)
    
    def test_11_void_sale_reverses_stock(self):
        """Test that voiding a sale creates RETURN movements and restores stock"""
        # Create a sale
        payload = {
            'cashier': 'Emma',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 10}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        sale_id = json.loads(response.data)['sale_id']
        
        with app.app_context():
            # Verify stock reduced
            product = Product.query.filter_by(sku='TEST001').first()
            stock_after_sale = product.get_current_stock()
            self.assertEqual(stock_after_sale, 40)  # 50 - 10
        
        # Void the sale
        void_payload = {
            'reason': 'Customer requested refund',
            'user': 'Manager'
        }
        
        response = self.client.post(
            f'/api/pos/sales/{sale_id}/void',
            data=json.dumps(void_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        with app.app_context():
            # Check sale marked as VOIDED
            sale = Sale.query.get(sale_id)
            self.assertEqual(sale.payment_status, 'VOIDED')
            
            # Check RETURN movement created
            returns = InventoryMovement.query.filter(
                InventoryMovement.sku == 'TEST001',
                InventoryMovement.movement_type == 'RETURN'
            ).all()
            self.assertEqual(len(returns), 1)
            self.assertEqual(returns[0].quantity, 10)
            
            # Check stock restored
            product = Product.query.filter_by(sku='TEST001').first()
            restored_stock = product.get_current_stock()
            self.assertEqual(restored_stock, 50)  # Back to original
    
    def test_12_void_already_voided_sale(self):
        """Test that voiding already voided sale returns error"""
        # Create and void a sale
        payload = {
            'cashier': 'Frank',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 5}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        sale_id = json.loads(response.data)['sale_id']
        
        # Void once
        void_payload = {'reason': 'Test', 'user': 'Tester'}
        self.client.post(
            f'/api/pos/sales/{sale_id}/void',
            data=json.dumps(void_payload),
            content_type='application/json'
        )
        
        # Try to void again
        response = self.client.post(
            f'/api/pos/sales/{sale_id}/void',
            data=json.dumps(void_payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('already voided', data['message'])
    
    def test_13_sales_list_api(self):
        """Test GET /api/pos/sales returns sales list"""
        # Create multiple sales
        for i in range(3):
            payload = {
                'cashier': f'Cashier{i}',
                'payment_method': 'CASH',
                'discount_tzs': 0,
                'items': [
                    {'sku': 'TEST001', 'qty': 1}
                ]
            }
            
            self.client.post(
                '/api/pos/sales',
                data=json.dumps(payload),
                content_type='application/json'
            )
        
        # Get sales list
        response = self.client.get('/api/pos/sales')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['count'], 3)
    
    def test_14_sales_list_filtering_by_date(self):
        """Test sales list filtering by date range"""
        # Create a sale
        payload = {
            'cashier': 'Grace',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 1}
            ]
        }
        
        self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Filter by today's date
        today = datetime.now().strftime('%Y-%m-%d')
        response = self.client.get(f'/api/pos/sales?from_date={today}&to_date={today}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['count'], 1)
    
    def test_15_invalid_payment_method(self):
        """Test that invalid payment method is rejected"""
        payload = {
            'cashier': 'Henry',
            'payment_method': 'INVALID_METHOD',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 1}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('Invalid payment method', data['message'])
    
    def test_16_empty_cart_checkout(self):
        """Test that empty cart checkout is rejected"""
        payload = {
            'cashier': 'Ivy',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': []
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('empty', data['message'].lower())
    
    def test_17_inactive_product_rejected(self):
        """Test that checkout rejects inactive products"""
        with app.app_context():
            # Deactivate a product
            product = Product.query.filter_by(sku='TEST001').first()
            product.is_active = False
            db.session.commit()
        
        payload = {
            'cashier': 'Jack',
            'payment_method': 'CASH',
            'discount_tzs': 0,
            'items': [
                {'sku': 'TEST001', 'qty': 1}
            ]
        }
        
        response = self.client.post(
            '/api/pos/sales',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('inactive', data['message'].lower())


if __name__ == '__main__':
    unittest.main()
