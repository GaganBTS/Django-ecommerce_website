from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render

from cart.cart import Cart
from .models import *


# Create your views here.
def payment_success(request):
    keys = list(request.session.keys())
    for key in keys:
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment/payment_success.html')


def payment_failed(request):
    return render(request, 'payment/payment_failed.html')


def checkout(request):
    if request.user.is_authenticated:
        try:
            shippingaddress = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shippingaddress}
            return render(request, 'payment/checkout.html', context)
        except:
            return render(request, 'payment/checkout.html')
    else:
        return render(request, 'payment/checkout.html')


def complete_order(request):
    if request.POST.get('action') == 'post':
        name = request.POST.get('name')

        address1 = request.POST.get('address1')
        landmark = request.POST.get('landmark')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')
        mobile = request.POST.get('mobile')
        shipping_address = f'{address1} near {landmark}, {city}, {state} \n {zipcode}'
        cart = Cart(request)
        total_cost = cart.get_total()
        # authenticated users
        if request.user.is_authenticated:
            order = Order.objects.create(full_name=name, mobile=mobile, shipping_address=shipping_address,
                                         amount=total_cost, user=request.user)
            order_id = order.pk
            products = []
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['qty'], user=request.user)
                products.append(item)
        # guest-users
        else:
            order = Order.objects.create(full_name=name, mobile=mobile, shipping_address=shipping_address,
                                         amount=total_cost)
            order_id = order.pk
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                         quantity=item['qty'])
        send_mail(f'Order Placed!', f'Your order for \n\n {str(products)} \n is placed successfully.\n Total paid'
                                    f' ${cart.get_total()}\nThanks'
                                    f'for shopping with us.', settings.EMAIL_HOST_USER, [email], fail_silently=False)

        order_success = True
        response = JsonResponse({'sucess': order_success})
        return response
