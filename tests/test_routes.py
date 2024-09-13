import unittest
from app import create_app, db
from app.models import Product, Category
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Protein Powder Comparison', response.data)

    def test_index_routes_with_filters(self):
        #create some test products
        category1 = Category(name='Whey Protein')
        category2 = Category(name='Plant Protein')
        product1 = Product(name='Whey Protein', brand = 'Brand A', type='Whey Protien', protein_per_serving=25.0, price=39.99, category=category1)
        product2 = Product(name='Pea Protein', brand='Brand B', type='Plant', protein_per_serving=20.0, price=29.99, category=category2)
        db.session.add_all([product1, product2])
        db.session.commit()

    def test_product_detail_route(self):
        category = Category(name='Whey Protein')
        product = Product(name='Test Protein', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        response = self.client.get(f'/product/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein', response.data)

    def test_compare_route(self):
        category = Category(name='Whey Protein')
        product1 = Product(name='Test Protein 1', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        product2 = Product(name='Test Protein 2', brand='Test Brand', type='Whey', protein_per_serving=30.0, price=49.99, category=category)
        db.session.add_all([product1, product2])
        db.session.commit()

        response = self.client.get(f'/compare?products={product1.id}&products={product2.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein 1', response.data)
        self.assertIn(b'Test Protein 2', response.data)
        
        # Test with brand filter
        response = self.client.get('/?brand=Brand+A')
        self.assertIn(b'Whey Isolate', response.data)
        self.assertNotIn(b'Pea Protein', response.data)

        # Test with price range filter
        response = self.client.get('/?price_range=20-40')
        self.assertIn(b'Whey Isolate', response.data)
        self.assertIn(b'Pea Protein', response.data)

        # Test with protein range filter
        response = self.client.get('/?protein_range=25%2B')  # 25+
        self.assertIn(b'Whey Isolate', response.data)
        self.assertNotIn(b'Pea Protein', response.data)

    def test_index_route_pagination(self):
        # Create more than one page of products
        category = Category(name='Test Category')
        for i in range(25):  # Assuming PRODUCTS_PER_PAGE is set to 15
            product = Product(name=f'Product {i}', brand='Test Brand', type='Test', protein_per_serving=20.0, price=30.00, category=category)
            db.session.add(product)
        db.session.commit()

        # Test first page
        response = self.client.get('/?page=1')
        self.assertIn(b'Product 0', response.data)
        self.assertIn(b'Next', response.data)
        self.assertNotIn(b'Previous', response.data)

        # Test second page
        response = self.client.get('/?page=2')
        self.assertIn(b'Product 12', response.data)
        self.assertIn(b'Previous', response.data)


    def test_product_detail_nonexistent_product(self):
        response = self.client.get('/product/9999')  # Assuming 9999 is a non-existent ID
        self.assertEqual(response.status_code, 404)

    def test_compare_route_with_invalid_ids(self):
        response = self.client.get('/compare?products=9999&products=10000')
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertIn('index', response.location)
        
    def test_search_route_no_results(self):
        response = self.client.get('/search?query=NonexistentProduct')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

        
    def test_search_route(self):
        category = Category(name='Whey Protein')
        product = Product(name='Test Protein', brand='Test Brand', type='Whey', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        response = self.client.get('/search?query=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Protein', response.data)
        
    def test_protein_101_route(self):
        response = self.client.get('/protein-101')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Protein 101: Your Complete Guide to Protein Powders', response.data)
        self.assertIn(b'Whey Protein', response.data)
        self.assertIn(b'Casein Protein', response.data)
        self.assertIn(b'Egg Protein', response.data)
        self.assertIn(b'Soy Protein', response.data)
        self.assertIn(b'Pea Protein', response.data)
        self.assertIn(b'Rice Protein', response.data)
        self.assertIn(b'Hemp Protein', response.data)

    # Admin route tests (if applicable)
    def test_admin_login(self):
        response = self.client.post('/admin/login', data={
        'username': 'admin',
        'password': 'password'
    }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)  # Assuming the admin page has this title
        self.assertIn(b'/admin/logout', response.data)  # Check for logout link to confirm logged in state

    def login(self, username='admin', password='password'):
        return self.client.post('/admin/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def test_admin_product_create(self):
    self.login()  # Log in before attempting to create a product
    response = self.client.post('/admin/product/create', data={
        'name': 'New Product',
        'brand': 'New Brand',
        'type': 'New Type',
        'protein_per_serving': 30.0,
        'price': 45.99
    }, follow_redirects=True)
    self.assertIn(b'Product added successfully', response.data)

    def test_admin_product_edit(self):
        # Create a product
        category = Category(name='Test Category')
        product = Product(name='Test Product', brand='Test Brand', type='Test', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        # Log in as admin and edit the product
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
        response = self.client.post(f'/admin/product/{product.id}/edit', data={
            'name': 'Updated Product',
            'brand': 'Updated Brand',
            'type': 'Updated Type',
            'protein_per_serving': 35.0,
            'price': 49.99
        }, follow_redirects=True)
        self.assertIn(b'Product updated successfully', response.data)

    def test_admin_product_delete(self):
        # Create a product
        category = Category(name='Test Category')
        product = Product(name='Test Product', brand='Test Brand', type='Test', protein_per_serving=25.0, price=39.99, category=category)
        db.session.add(product)
        db.session.commit()

        # Log in as admin and delete the product
        self.client.post('/admin/login', data={'username': 'admin', 'password': 'password'})
        response = self.client.post(f'/admin/product/{product.id}/delete', follow_redirects=True)
        self.assertIn(b'Product deleted successfully', response.data)

if __name__ == '__main__':
    unittest.main()