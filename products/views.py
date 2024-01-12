import stripe

from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings

from accounts.models import Address

from .models import Product, Cart, Order
from .forms import ProductForm, ProductFilterForm



def index(request):
    products = Product.objects.all()

    if request.method == "GET":
        form = ProductFilterForm(request.GET)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            category = form.cleaned_data.get('category')

            if name:
                products = products.filter(name__icontains=name)
            if min_price:
                products = products.filter(cost__gte=min_price)
            if max_price:
                products = products.filter(cost__lte=max_price)
            if category:
                products = products.filter(category=category)

    else:
        form = ProductFilterForm()


    context = {
        'products':products,
        'form':form
    }

    return render(request, 'index.html', context)


@login_required
def new_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    
    context = {
        'form':form
    }

    return render(request, 'new_product.html', context)


def product(request, id):
    product = Product.objects.get(id=id)

    return render(request, 'product.html', {'product':product})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.user:
        return HttpResponseForbidden('You can not delete this product!')

    if request.method == 'POST':
        product.delete()
        return redirect('home')
    
    return render(request, 'delete_product.html', {'product': product})


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user != product.user:
        return HttpResponseForbidden('You can not edit this product!')

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = ProductForm(instance=product)

    context = {
        'product':product,
        'form':form
    }

    return render(request, 'edit_product.html', context)


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.cost * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item, created = Cart.objects.get_or_create(product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def reduce_quantity(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart_item = get_object_or_404(Cart, product=product)
    cart_item.quantity -= 1        
    cart_item.save()

    if cart_item.quantity == 0:
        cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, user=request.user, product__pk=pk)
    cart_item.delete()
    
    return redirect('cart')


# buyurtma berish
# def order(request):
#     cart_objects = Cart.objects.filter(user=request.user)

#     addresses = Address.objects.filter(user=request.user)

#     for cart_object in cart_objects:
#         cart_object.total_cost = cart_object.product.cost * cart_object.quantity

#     context = {
#         'cart_objects':cart_objects, 
#         'addresses':addresses,
#     }

#     if request.method == 'POST':
#         address_id = request.POST.get('address', '')
#         selected_address = get_object_or_404(Address, id=address_id)
#         phone = request.POST.get('phone', '')

#         for cart_object in cart_objects:
#             new_order = Order(
#                 product = cart_object.product,
#                 cost = cart_object.product.cost * cart_object.quantity,
#                 quantity = cart_object.quantity,
#                 customer = cart_object.user,
#                 address = selected_address,
#                 phone = phone
#             )

#             new_order.save()
#             cart_object.delete()

#         # new orders = []

#         return render(request, 'orders/order_created.html', context)


#     return render(request, 'orders/place_order.html', context)


stripe.api_key = settings.STRIPE_PRIVATE_KEY

@login_required
@require_POST
def create_stripe_checkout_session(request):
    cart_objects = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    # Calculate total cost for each item in the cart
    for cart_object in cart_objects:
        cart_object.total_cost = cart_object.product.cost * cart_object.quantity

    # Your existing context data
    context = {
        'cart_objects': cart_objects,
        'addresses': addresses,
    }

    # Handle the checkout process
    address_id = request.POST.get('address', '')
    selected_address = get_object_or_404(Address, id=address_id)
    phone = request.POST.get('phone', '')

    # Create a list to store order details

    try:
        # Create a Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': cart_object.product.name,
                            'description': cart_object.product.description,
                        },
                        'unit_amount': int(cart_object.product.cost * 100),  # Stripe uses cents
                    },
                    'quantity': cart_object.quantity,
                }
                for cart_object in cart_objects
            ],
            mode='payment',
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        # Create an order for each item in the cart
        for cart_object in cart_objects:
            new_order = Order(
                product=cart_object.product,
                cost=cart_object.product.cost * cart_object.quantity,
                quantity=cart_object.quantity,
                customer=cart_object.user,
                address=selected_address,
                phone=phone
            )
            new_order.save()
            # new_orders.append(new_order)

        # Save the orders
        # Order.objects.bulk_create(new_orders)

        # Redirect to Stripe Checkout
        return redirect(checkout_session.url)

    except stripe.error.StripeError as e:
        # Handle errors, you might want to log or show an error message to the user
        return render(request, 'orders/error.html', {'error': str(e)})
    

@login_required
def place_order(request):
    cart_objects = Cart.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)

    # Calculate total cost for each item in the cart
    for cart_object in cart_objects:
        cart_object.total_cost = cart_object.product.cost * cart_object.quantity

    context = {
        'cart_objects': cart_objects,
        'addresses': addresses,
    }

    return render(request, 'orders/place_order.html', context)


def orders(request):
    orders = Order.objects.filter(customer=request.user, is_active=True)
    context = {'orders':orders}

    return render(request, 'orders/orders.html', context)


def success(request):
    return render(request, 'orders/order_created.html')

def fail(request):
    return render(request, 'orders/order_failed.html')


#buyurtmani yakunlash
def complete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    
    if not order.is_delivered:
        order.complete_order()
        print(order.is_delivered)
        return render(request, 'orders/order_completed.html', {'order': order})

    return render(request, 'orders/order_completed.html', {'order': order})