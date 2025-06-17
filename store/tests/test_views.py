# python manage.py test store

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from store.models import User, Store, Product, Order, OrderItem, Review

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.vendor = User.objects.create_user(username='vendor',
                                               password='testpass',
                                               role=User.VENDOR)
        self.buyer = User.objects.create_user(username='buyer',
                                              password='testpass',
                                              role=User.BUYER)
        self.store = Store.objects.create(owner=self.vendor,
                                          name='Vendor Store')
        self.product = Product.objects.create(store=self.store,
                                              name='Test Product',
                                              price=10.00,
                                              stock=100)


class AuthTests(BaseTestCase):
    def test_register_buyer(self):
        response = self.client.post(reverse('register'), {
            'username': 'newbuyer',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',
            'role': User.BUYER
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newbuyer').exists())

    def test_login_vendor(self):
        login = self.client.login(username='vendor', password='testpass')
        self.assertTrue(login)


class ProductStoreViewsTests(BaseTestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_all_products_view(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        response = self.client.get(reverse('product_detail',
                                           args=[self.product.id])
                                   )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_vendor_manage_store_requires_login(self):
        response = self.client.get(reverse('manage_store'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_vendor_manage_store_access(self):
        self.client.login(username='vendor', password='testpass')
        response = self.client.get(reverse('manage_store'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vendor Store')


class CartCheckoutTests(BaseTestCase):
    def test_add_to_cart(self):
        self.client.login(username='buyer', password='testpass')
        response = self.client.get(reverse('add_to_cart',
                                           args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn(str(self.product.id), session.get('cart', {}))

    def test_view_cart(self):
        self.client.login(username='buyer', password='testpass')
        session = self.client.session
        session['cart'] = {str(self.product.id): 2}
        session.save()
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_checkout_requires_buyer(self):
        self.client.login(username='vendor', password='testpass')
        response = self.client.get(reverse('checkout'))
        self.assertContains(response, "Only buyers can checkout.")

    def test_checkout_empty_cart(self):
        self.client.login(username='buyer', password='testpass')
        response = self.client.get(reverse('checkout'))
        self.assertContains(response, "Cart is empty.")


class OrderReviewTests(BaseTestCase):
    def test_order_history(self):
        self.client.login(username='buyer', password='testpass')
        Order.objects.create(user=self.buyer)
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 200)

    def test_submit_review(self):
        self.client.login(username='buyer', password='testpass')
        Order.objects.create(user=self.buyer)
        response = self.client.post(
            reverse('submit_review', args=[self.product.id]),
            {'rating': 5, 'comment': 'Great!'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(product=self.product,
                                              user=self.buyer).exists()
                        )


class VendorActionsTests(BaseTestCase):
    def test_create_store(self):
        self.client.login(username='vendor', password='testpass')
        response = self.client.post(reverse('create_store'),
                                    {'name': 'New Store'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Store.objects.filter(name='New Store').exists())

    def test_create_product(self):
        self.client.login(username='vendor', password='testpass')
        response = self.client.post(
            reverse('create_product', args=[self.store.id]),
            {'name': 'Another Product', 'price': 20, 'stock': 5}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='Another Product').exists())


class PermissionsTests(BaseTestCase):
    def test_buyer_cannot_manage_store(self):
        self.client.login(username='buyer', password='testpass')
        response = self.client.get(reverse('manage_store'))
        self.assertEqual(response.status_code, 403)

    def test_vendor_cannot_checkout(self):
        self.client.login(username='vendor', password='testpass')
        response = self.client.get(reverse('checkout'))
        self.assertContains(response, "Only buyers can checkout.")
