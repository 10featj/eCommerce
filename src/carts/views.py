from django.shortcuts import render, redirect
from .models import Cart
from django.contrib import messages
from products.models import Product
from orders.models import Order


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
    return render(request, "carts/checkout.html", {"object": order_obj})


    # cart_id = request.session.get('cart_id', None)
    # qs = Cart.objects.filter(id=cart_id)
    # if qs.count() == 1:
    #     print('Cart Id Exists')
    #     cart_obj = qs.first()
    #     if request.user.is_authenticated() and cart_obj.user is None:
    #         cart_obj.user = request.user
    #         cart_obj.save()
    # else:
    #     cart_obj = Cart.objects.new(user=request.user)
    #     request.session['cart_id'] = cart_obj.id


    # print(request.session) # session is on the request method
    # print(dir(request.session))
    # key = request.session.session_key(300) # 5 minutes
    # key = request.session.set_expiry
    # key = request.session.session_key
    # print(key)
    # Storing a session variable/ Getting
    # request.session['first_name'] = "Jordan" # Setter
    # print(request.session.get('first_name', 'Unknown')) # Getter
