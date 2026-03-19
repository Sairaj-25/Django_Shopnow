import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.shop.models import Category, Product, CartItem
from apps.shop.forms import CustomerForm


class CategoryModelTest(TestCase):
    def test_category_str(self):
        category = Category.objects.create(name="Fruits", slug="fruits")
        self.assertEqual(str(category), "Fruits")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Veg", slug="veg")

    def test_product_str(self):
        p = Product.objects.create(
            name="Carrot", category=self.category, price=100, stock_quantity=10
        )
        self.assertEqual(str(p), "Carrot")

    def test_product_is_in_stock(self):
        p = Product.objects.create(
            name="Potato",
            category=self.category,
            price=80,
            stock_quantity=5,
        )
        self.assertTrue(p.is_in_stock)

    def test_slug_auto_generation(self):
        p = Product.objects.create(
            name="Tomato",
            category=self.category,
            price=50,
            stock_quantity=8,
        )
        self.assertTrue(p.slug.startswith("tomato"))


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="pass")
        cat = Category.objects.create(name="ABC", slug="abc")
        self.product = Product.objects.create(
            name="Prod", category=cat, price=20, stock_quantity=10
        )

    def test_cart_item_total_price(self):
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=3
        )
        self.assertEqual(cart_item.get_total_price(), 60)

    def test_cart_item_auto_delete_on_zero_quantity(self):
        """Test that a cart item deletes itself if quantity drops below 1."""
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=1
        )
        cart_item.quantity = 0
        cart_item.save()
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())


class ShopFormTests(TestCase):
    def test_customer_form_valid(self):
        """Test that the customer form accepts valid data."""
        form_data = {
            "name": "John Doe",
            "phone": "1234567890",
            "address": "123 Test Street",
            "city": "Pune",
            "state": "Maharashtra",
            "pin_code": "411045",
            "landmark": "Near Stadium",
        }
        form = CustomerForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_customer_form_invalid_phone_and_pin(self):
        """Test that the custom regex validators catch invalid phone numbers and pin codes."""
        form_data = {
            "name": "John Doe",
            "phone": "12345",  # Too short
            "address": "123 Test Street",
            "city": "Pune",
            "state": "Maharashtra",
            "pin_code": "41104",  # Too short
        }
        form = CustomerForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertIn("pin_code", form.errors)


class ShopViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="guest", password="guestpass")
        self.category = Category.objects.create(name="TestCat", slug="testcat")
        self.product = Product.objects.create(
            name="Test Product", category=self.category, price=100, stock_quantity=5
        )

    def test_home_view_status_code(self):
        # Using "/" instead of reverse("home") since urls.py lacks name="home"
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "Index.html")
        self.assertIn("products", response.context)

    def test_product_info_view(self):
        url = reverse("product_info", args=[self.product.id])
        response = self.client.get(url)
        self.assertContains(response, "Test Product")

    def test_add_to_cart_requires_login(self):
        # Should redirect to login if not logged in
        response = self.client.post(
            reverse("add_to_cart"), {}, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 302)

    def test_add_to_cart_logged_in(self):
        self.client.login(username="guest", password="guestpass")
        response = self.client.post(
            reverse("add_to_cart"),
            data=json.dumps(
                {"product_id": self.product.id}
            ),  # Converted to JSON payload
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Added to cart", response.json().get("message"))

    def test_cart_page_after_adding(self):
        self.client.login(username="guest", password="guestpass")
        self.client.post(
            reverse("add_to_cart"),
            data=json.dumps(
                {"product_id": self.product.id}
            ),  # Converted to JSON payload
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        response = self.client.get(reverse("cart"))
        self.assertContains(response, "Test Product")
        self.assertEqual(response.context["Total"], 100.00)

    def test_update_quantity_increment(self):
        """Test incrementing cart quantity via the standard HTML form."""
        self.client.login(username="guest", password="guestpass")
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=1
        )

        url = reverse("update_quantity", args=[self.product.id, "increment"])

        # We pass HTTP_REFERER because your view uses request.META.get("HTTP_REFERER", "/") to redirect
        response = self.client.post(url, HTTP_REFERER="/cart/")

        # Verify it redirects back to the cart page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/cart/", fetch_redirect_response=False)

        # Refresh from DB and check if quantity increased
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 2)

    def test_update_quantity_decrement(self):
        """Test decrementing cart quantity via the standard HTML form."""
        self.client.login(username="guest", password="guestpass")
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=2
        )

        url = reverse("update_quantity", args=[self.product.id, "decrement"])
        response = self.client.post(url, HTTP_REFERER="/cart/")

        self.assertEqual(response.status_code, 302)

        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 1)

    def test_update_quantity_decrement_to_zero(self):
        """Test that decrementing a quantity of 1 deletes the cart item."""
        self.client.login(username="guest", password="guestpass")
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=1
        )

        url = reverse("update_quantity", args=[self.product.id, "decrement"])
        response = self.client.post(url, HTTP_REFERER="/cart/")
        self.assertEqual(response.status_code, [200, 302])
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

        # The view subtracts 1, making it 0.
        # Your custom CartItem.save() method should automatically delete it.
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    def test_ajax_update_cart_increment(self):
        """Test the AJAX update_cart endpoint for incrementing."""
        self.client.login(username="guest", password="guestpass")
        CartItem.objects.create(user=self.user, product=self.product, quantity=1)

        response = self.client.post(
            reverse("update_cart"),
            data=json.dumps({"product_id": self.product.id, "action": "increment"}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("quantity"), 2)

    def test_ajax_update_cart_decrement_to_zero(self):
        """Test the AJAX update_cart endpoint for removing an item."""
        self.client.login(username="guest", password="guestpass")
        cart_item = CartItem.objects.create(
            user=self.user, product=self.product, quantity=1
        )

        response = self.client.post(
            reverse("update_cart"),
            data=json.dumps({"product_id": self.product.id, "action": "decrement"}),
            content_type="application/json",
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("quantity"), 0)
        self.assertEqual(response.json().get("message"), "Removed from cart")

        # Verify it was actually deleted from the database
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())
