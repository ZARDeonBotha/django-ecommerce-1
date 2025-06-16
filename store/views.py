from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from store.models import Product, Order, OrderItem, Review
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse
from .models import Order, OrderItem, Product, User
from .models import Store, User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ProductForm, StoreForm
from .models import User, Store

User = get_user_model()


# Create your views here.
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('all_products')


from django.http import HttpResponse


def home(request):
    # Fetch products from the database to display
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

@login_required
def checkout(request):
    if request.user.role != User.BUYER:
        return HttpResponse("Only buyers can checkout.")

    cart = request.session.get('cart', {})
    if not cart:
        return HttpResponse("Cart is empty.")

    order = Order.objects.create(user=request.user)
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )
        # Reduce stock
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


def submit_review(request, product_id):
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
    return render(request, 'submit_review.html', {'product': product})


@login_required
def manage_store(request):
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can manage stores.", status=403)
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'store/manage_store.html', {'stores': stores})


@login_required
def view_cart(request):
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
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')


@login_required
def update_cart_quantity(request, product_id):
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
def vendor_store_list(request):
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can view their stores.", status=403)
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'store/store_list.html', {'stores': stores})


@login_required
def vendor_product_list(request, store_id):
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can manage products.", status=403)
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = Product.objects.filter(store=store)
    return render(request, 'store/vendor_product_list.html',
                  {'store': store, 'products': products})

def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/all_products.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    reviews = product.review_set.all()
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

@login_required
def vendor_store_list(request):
    stores = Store.objects.filter(owner=request.user)
    return render(request, 'store/vendor_store_list.html', {'stores': stores})

@login_required
def vendor_orders(request):
    if request.user.role != User.VENDOR:
        return HttpResponse("Only vendors can view store orders.", status=403)
    stores = Store.objects.filter(owner=request.user)
    orders = Order.objects.filter(items__product__store__in=stores).distinct()
    return render(request, 'store/vendor_orders.html', {'orders': orders})

@login_required
def create_product(request, store_id):
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
    return render(request, 'store/product_form.html', {'form': form, 'store': store})

@login_required
def create_store(request):
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
    return render(request, 'store/store_form.html', {'form': form})

