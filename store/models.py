from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Represents a user with specific roles such as Vendor or Buyer.

    This class extends the AbstractUser class and introduces an
    additional role attribute that specifies whether the user is a
    Vendor or a Buyer. It provides functionality to categorize users based
    on their roles for specific application
    needs.

    :ivar role: The role of the user, either Vendor ('V') or Buyer ('B').
    :type role: CharField
    """
    VENDOR = 'V'
    BUYER = 'B'
    ROLE_CHOICES = [(VENDOR, 'Vendor'), (BUYER, 'Buyer')]
    role = models.CharField(max_length=1,
                            choices=ROLE_CHOICES,
                            default=BUYER)


class Store(models.Model):
    """
    Represents a store managed by a user.

    This class defines the properties and behaviors of a store
    in the system. Each store is owned by a user and has a name
    and a timestamp indicating when it was created.

    :ivar owner: The user who owns the store.
    :type owner: models.ForeignKey
    :ivar name: The name of the store.
    :type name: models.CharField
    :ivar created_at: The timestamp of when the store was created.
    :type created_at: models.DateTimeField
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    """
    Represents a product available in the store.

    The Product class is designed to store information about items
    available in a store. It includes details about the item's name, price,
    stock level, and additional properties
    such as an image and description.
    Products are associated with a specific store and can be managed within
    the database.

    :ivar store: The store to which the product belongs.
    :type store: ForeignKey
    :ivar name: The name of the product, up to 100 characters.
    :type name: CharField
    :ivar price: The price of the product as a decimal value.
    :type price: DecimalField
    :ivar stock: The number of items available in stock.
    :type stock: PositiveIntegerField
    :ivar image: An optional image associated with the product.
        It supports null and blank values.
    :type image: ImageField
    :ivar description: An optional textual description of the product.
        It supports blank values.
    :type description: TextField
    """
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    description = models.TextField(blank=True)


class Order(models.Model):
    """
    Represents an order placed by a user in the system.

    This class stores information about an order, including the user who
    placed it and  the timestamp when it was created. It is used to link
    orders to users and to manage
    the creation history of these orders.

    :ivar user: The user who placed the order.
    :type user: ForeignKey
    :ivar created_at: The timestamp when the order was created.
    :type created_at: DateTimeField
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    """
    Represents an individual item within an order.

    This model defines the relationship between an order and the products
    associated with it. Each item includes details about the quantity and
    price of the product within the order.

    :ivar order: The order to which this item belongs. Establishes a
        foreign key relationship with the `Order` model.
    :type order: ForeignKey
    :ivar product: The product associated with this item. Establishes a
        foreign key relationship with the `Product` model.
    :type product: ForeignKey
    :ivar quantity: The quantity of the product within the order.
    :type quantity: PositiveIntegerField
    :ivar price: The price of the product within the order, stored with
        a specific decimal precision.
    :type price: DecimalField
    """
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    """
    Represents a review given by a user for a specific product.

    Handles data related to user reviews, including a rating, a comment,
    and additional metadata such as the creation timestamp and whether
    the purchase was verified.

    :ivar product: The product being reviewed.
    :type product: ForeignKey
    :ivar user: The user who created the review.
    :type user: ForeignKey
    :ivar rating: The rating score given by the user, ranging from 1 to 5.
    :type rating: PositiveIntegerField
    :ivar comment: The text of the review provided by the user.
    :type comment: TextField
    :ivar created_at: The timestamp indicating when the review was created.
    :type created_at: DateTimeField
    :ivar verified_purchase: Indicates whether the review corresponds to a
        verified purchase.
    :type verified_purchase: BooleanField
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified_purchase = models.BooleanField(default=False)
