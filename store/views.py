from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProductForm, StoreForm
from .models import User, Store, Product, Review, Order, OrderItem
from rest_framework import viewsets, permissions
from .serializers import StoreSerializer, ProductSerializer, ReviewSerializer


User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    A custom user creation form.

    This class extends the default UserCreationForm to include
    additional fields such as 'email' and 'role'. It is designed for
    creating new user instances with these additional attributes while
    maintaining compatibility with the standard user creation process.

    :ivar Meta: Inner meta class for model and fields configuration.
    :type Meta: type
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def register(request: HttpRequest) -> HttpResponse:
    """
    Handles user registration by processing user input through a custom
    user creation form. If the request method is POST, validates and saves
    the user. Upon successful registration, logs the user in and redirects
    to the home page. Otherwise, renders the registration form.

    :param request: The HTTP request sent by the client, either containing
        user registration data in a POST request or used for displaying the
        form during a GET request.
    :type request: HttpRequest
    :return: An HTTP response that either redirects the user to the home
        page after successful registration or renders the registration form.
    :rtype: HttpResponse
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request,
                  'registration/register.html',
                  {'form': form}
                  )


def add_to_cart(request: HttpRequest, product_id: int) -> HttpResponseRedirect:
    """
    Handles adding a product to the shopping cart. Retrieves the cart
    from the user's session and increments the quantity of the specified
    product. If the cart does not exist in the session, it initializes
    a new cart. After updating the cart, the user is redirected to the
    "all_products" page.

    :param request: HttpRequest object containing metadata about the request
        from the user.
    :type request: HttpRequest
    :param product_id: ID of the product to be added to the cart.
    :type product_id: int
    :return: An HttpResponseRedirect to the "all_products" page.
    :rtype: HttpResponseRedirect
    """
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('all_products')


from django.http import HttpResponse


def home(request: HttpRequest) -> HttpResponse:
    """
    Fetches and displays all products from the database on the home page.

    This function queries the Product model for all available products
    and then passes the fetched data to the 'store/home.html' template for
    rendering. The resulting page showcases the products to the end-users.

    :param request:
        The HTTP request object containing metadata about the request.
    :return:
        The HTTP response object that renders the 'store/home.html' template
        populated with the list of products.
    """
    products = Product.objects.all()
    return render(request,
                  'store/home.html',
                  {'products': products}
                  )


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    """
    Handles the checkout process for a logged-in buyer user.
    Prevents negative stock and database errors by validating inventory.
    """
    if request.user.role != User.BUYER:
        return HttpResponse("Only buyers can checkout.")

    cart = request.session.get('cart', {})
    if not cart:
        return HttpResponse("Cart is empty.")

    # Check stock for all products before creating the order
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        if product.stock < quantity:
            return HttpResponse(
                f"Not enough stock for {product.name}. "
                f"Only {product.stock} left."
            )

    # All stock is sufficient, proceed with order creation
    order = Order.objects.create(user=request.user)
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        product.stock -= quantity
        product.save()

    # Clear the cart
    request.session['cart'] = {}

    # Send invoice email (simplified)
    send_mail(
        subject="Your Invoice",
        message=f"Thank you for your purchase! Order #{order.id}",
        from_email="yourshop@example.com",
        recipient_list=[request.user.email]
    )

    return render(request, 'checkout.html')


def submit_review(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Handles submission of a review for a specific product. This view
    function validates the user's purchase for product verification,
    processes the review data provided by the user, and saves it in
    the database. If the submission is successful, the user is redirected to
    the product detail page. Otherwise, it renders a template for submitting
    the review.

    :param request: The HTTP request object carrying user request data,
        including method and user details.
    :param product_id: The unique identifier of the product for which
        the review is being submitted.
    :return: An HttpResponse either rendering the review submission
        page or redirecting the user to the product detail page after
        successful submission.
    """
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        comment = request.POST['comment']
        # Check if user purchased this product
        verified = OrderItem.objects.filter(order__user=request.user,
                                            product=product).exists()
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment,
            verified_purchase=verified
        )
        return redirect('product_detail', product_id=product.id)
    return render(request,
                  'submit_review.html',
                  {'product': product}
                  )


@login_required
def manage_store(request: HttpRequest) -> HttpResponse:
    """
    Manages the store dashboard for the logged-in vendor user.
    This function renders a page where vendors can view and manage their
    associated stores.
    Access is restricted to authenticated users with a vendor role.

    :param request: The HTTP request object containing metadata about the
                    request and user information.
    :type request: HttpRequest
    :return: HTTP response object that includes the rendered manage
        store page or a 403 forbidden response if the user is not a vendor.
    :rtype: HttpResponse
    """
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can manage stores.",
                            status=403
                            )
    stores = Store.objects.filter(owner=request.user)
    return render(request,
                  'store/manage_store.html',
                  {'stores': stores}
                  )


@login_required
def view_cart(request: HttpRequest) -> HttpResponse:
    """
    Handles the display of the user's shopping cart and calculates
    the total cost of items within the cart. It retrieves product
    information as well as computes
    the subtotal for each product based on its price and quantity.

    :param request: Django HTTP request object used for retrieving
        the session and rendering the response.
    :type request: HttpRequest
    :return: HttpResponse object containing the rendered cart page with the
        list of cart items and the total cost.
    :rtype: HttpResponse
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })
        total += subtotal
    return render(request, 'cart.html',
                  {'cart_items': cart_items, 'total': total})


@login_required
def remove_from_cart(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Removes a product from the user's shopping cart stored in the session.

    This function checks if a specific product exists in the user's current
    session-based shopping cart by its product ID and removes it if
    present.
    The updated cart information is then saved back into the session.
    After modification, the user is redirected to the cart view page.

    :param request: The HTTP request object containing session data
        and user information.
    :type request: HttpRequest
    :param product_id: The ID of the product to be removed from the cart.
    :type product_id: int
    :return: An HTTP response redirecting the user to the cart view page.
    :rtype: HttpResponse
    """
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def update_cart_quantity(request: HttpRequest,
                         product_id: int) -> HttpResponseRedirect:
    """
    Updates the quantity of a specific product in the shopping cart.

    This function allows a logged-in user to update the quantity
    of a product in their session-based shopping cart. If the quantity is
    greater than zero, the cart is updated with the new quantity. If the
    quantity is zero or less, the product is removed from the cart. If the
    product is not already in the
    cart, no action is taken.

    :param request: The incoming HTTP request object containing session
        data and POST data with the updated quantity.
    :type request: HttpRequest
    :param product_id: The identifier of the product whose quantity is being
        updated in the cart.
    :type product_id: int
    :return: A redirect response to the 'view_cart' view.
    :rtype: HttpResponseRedirect
    """
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            if quantity > 0:
                cart[str(product_id)] = quantity
            else:
                del cart[str(product_id)]
            request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def vendor_store_list(request: HttpRequest) -> HttpResponse:
    """
    Handles the view for displaying a list of stores owned by the
    logged-in vendor.

    This view is restricted to users with the role of 'vendor'.
    Any attempt to access this view by non-vendor users will result in an
    HTTP 403 Forbidden
    response. The view retrieves and displays all stores associated with the
    currently logged-in vendor.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :return: An HTTP response containing the rendered template with a
        list of stores owned by the vendor.
    :rtype: HttpResponse
    """
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can view their stores.",
                            status=403)
    stores = Store.objects.filter(owner=request.user)
    return render(request,
                  'store/store_list.html',
                  {'stores': stores}
                  )


@login_required
def vendor_product_list(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Retrieves and displays the list of products for a specific store
    associated with the vendor. Only users with the role of "VENDOR" are
    permitted to
    access and manage the product list.

    :param request: The HTTP request object containing request metadata,
        including the current authenticated user.
    :type request: HttpRequest
    :param store_id: The unique identifier for the store whose products
        are to be managed by the vendor.
    :type store_id: int
    :return: An HTTP response containing the rendered product list page or
        a response with an appropriate status if the user is not authorized.
    :rtype: HttpResponse
    """
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can manage products.",
                            status=403)
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = Product.objects.filter(store=store)
    return render(request, 'store/vendor_product_list.html',
                  {'store': store, 'products': products})


def all_products(request: HttpRequest) -> HttpResponse:
    """
    Retrieve and display all products available in the database.

    This view fetches all instances of the Product model from the database
    and renders them into an HTML template for display.

    :param request: The HTTP request object received from the user.
    :type request: HttpRequest
    :return: An HTTP response object containing the rendered template with
        all products.
    :rtype: HttpResponse
    """
    products = Product.objects.all()
    return render(request,
                  'store/all_products.html',
                  {'products': products}
                  )


def product_detail(request: HttpRequest, product_id: int) -> HttpResponse:
    """
    Fetches and displays the details of a specific product along with
    its associated reviews.

    :param request: The HTTP request object containing metadata about
        the request.
    :type request: HttpRequest
    :param product_id: The unique identifier of the product to be fetched.
    :type product_id: int
    :return: An HTTP response object containing the rendered product
        detail page with the product information and its reviews.
    :rtype: HttpResponse
    """
    product = Product.objects.get(id=product_id)
    reviews = product.review_set.all()
    return render(request,
                  'store/product_detail.html',
                  {'product': product,
                   'reviews': reviews}
                  )


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    """
    Fetches the order history for the currently logged-in user
    and renders it on the order history page. The function queries the
    database for all orders associated with the authenticated user and
    passes the data to the specified
    HTML template for rendering.

    :param request: The HTTP request object representing the current
        request, which must be initiated by a logged-in user.
    :type request: HttpRequest
    :return: An HTTP response containing the rendered order history
        template with the user's orders.
    :rtype: HttpResponse
    """
    orders = Order.objects.filter(user=request.user)
    return render(request,
                  'store/order_history.html',
                  {'orders': orders}
                  )


@login_required
def vendor_store_list(request: HttpRequest) -> HttpResponse:
    """
    Render a list of stores belonging to the currently authenticated vendor.

    This view retrieves the list of stores associated with the current
    user (who is authenticated as a vendor) and renders them in the
    `vendor_store_list.html` template.

    :param request: The HTTP request object containing metadata about
        the request. It includes information about the authenticated user.
    :type request: HttpRequest
    :return: HTTP response with rendered content of the vendor's store
        list page.
    :rtype: HttpResponse
    """
    stores = Store.objects.filter(owner=request.user)
    return render(request,
                  'store/vendor_store_list.html',
                  {'stores': stores}
                  )


@login_required
def vendor_orders(request: HttpRequest) -> HttpResponse:
    """
    Handles the retrieval of orders related to the stores owned by
    the currently logged-in vendor. This view restricts access to
    users with the vendor role and ensures that only orders associated with
    their stores are displayed.

    :param request: The HTTP request object containing metadata about
        the request and the user's session.
    :types request: HttpRequest
    :return: An HTTP response containing rendered vendor-specific
        order details or a 403 response if the user is not a vendor.
    :rtype: HttpResponse
    """
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can view store orders.",
                            status=403)
    stores = Store.objects.filter(owner=request.user)
    orders = Order.objects.filter(items__product__store__in=stores).distinct()
    return render(request,
                  'store/vendor_orders.html',
                  {'orders': orders})


@login_required
def create_product(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Handles the creation of a new product for a specific store.
    This function ensures that the store exists, belongs to the currently
    authenticated user, and processes the form submission for the
    new product. Depending on the HTTP request method, it either displays
    the product form or processes and saves the submitted form data.

    :param request: The HTTP request object, which contains metadata
        about the request. It is also used to check the authenticated user
        and validate ownership of the store.
    :type request: HttpRequest
    :param store_id: The unique identifier of the store where the
        product is being created. Used to associate the new product
        with the correct store.
    :type store_id: int
    :return: An HTTP response which either renders the product form
        for a GET request or redirects to the 'manage_store' view upon
        successful form submission.
    :rtype: HttpResponse
    """
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store  # Assign the store here
            product.save()
            return redirect('manage_store')
    else:
        form = ProductForm()
    return render(request,
                  'store/product_form.html',
                  {'form': form, 'store': store}
                  )


@login_required
def create_store(request: HttpRequest) -> HttpResponse:
    """
    Handles the creation of a new store for vendors. This view
    renders a form to create a store and processes form submissions. It
    restricts access to only users with a VENDOR role and ensures the
    created store is associated with the logged-in user.

    :param request: The HTTP request object containing metadata about
        the request.
    :type request: HttpRequest
    :return: An HTTP response with either a rendered store creation
        form or a response indicating the outcome of the store creation
        process.
    :rtype: HttpResponse
    """
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can add stores.", status=403)
    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()
            return redirect('vendor_store_list')
    else:
        form = StoreForm()
    return render(request,
                  'store/store_form.html',
                  {'form': form})
