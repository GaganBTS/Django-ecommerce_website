from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from store.models import *
from .cart import Cart


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})


def cart_add(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product, product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'product_title': product.title, 'product_qty': cart_qty})
        print(response)
        return response


def cart_delete(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        cart_qty = cart.__len__()
        # cart_total = cart.get_total()
        response = JsonResponse({'qty': cart_qty})
        return response


def cart_update(request):
    cart = Cart(request=request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, product_qty=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty': cart_qty})
        return response
