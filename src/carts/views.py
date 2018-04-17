from django.shortcuts import render, redirect
from .models import Cart
from django.contrib import messages
from products.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    product_obj = ''
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.add_message(request, messages.ERROR,
                                 'Product not found :(. Go back to <a href="/products/">Products</a>! ')
            return redirect('cart:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            messages.add_message(request, messages.SUCCESS,
                                 'Product removed from <a href="/cart/">Cart</a>!')
        else:
            cart_obj.products.add(product_obj)
            messages.add_message(request, messages.SUCCESS,
                                 'Product added to <a href="/cart/">Cart</a>!')
        request.session['cart_items'] = cart_obj.products.count()
    # cart_obj.products.remove(product_obj)
    # return redirect(product_obj.get_absolute_url())
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    else:
        order_obj, new_order_obj = Order.objects.get_or_create(cart=cart_obj)
    user = request
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()

    if request.user.is_authenticated():
        if request.user.email:
            billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(
                user=request.user,
                email=request.user.email,
            )
            print(request.user.email)

    context = {
        "object": new_order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form
    }

    return render(request, "carts/checkout.html", context)


