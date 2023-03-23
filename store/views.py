from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy

from payment.models import OrderItem
from .models import *


# Create your views here.


def categories(request):
    all_ctg = Category.objects.all()
    return {'all_ctg': all_ctg}


def store(request):
    if request.method == 'GET':
        products = Product.objects.all()
        return render(request, 'store/store.html', {"products": products})
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            url = reverse_lazy('store')
            return HttpResponseRedirect(url)
        except Exception as e:
            messages.error(request, message='Invalid username or password')
            url = reverse_lazy('login')
            return HttpResponseRedirect(url)


def productinfo(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = Reviews.objects.filter(product=product)
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user)
    else:
        wishlist = []
    context = {'product': product, 'wishlist': wishlist, 'reviews': reviews, 'orders': OrderItem}
    return render(request, 'store/product-info.html', context)


def listcategory(request, slug):
    products = Product.objects.filter(category__slug=slug)
    return render(request, 'store/list-category.html', {'products': products, 'ctg': slug})


@login_required(login_url='login')
def wishlist(request):
    if request.method == 'GET':
        wl = Wishlist.objects.filter(user=request.user)
        context = {'wishlist': wl}
        return render(request, 'store/wishlist.html', context)
    if request.method == 'POST':
        if request.POST.get('action') == 'post':
            product_id = request.POST.get('product_id')
            product = Product.objects.get(id=product_id)
            v = get_object_or_404(Wishlist, product=product)
            if v != None:
                response = {'success': False}
                return JsonResponse(response)
            else:
                Wishlist.objects.create(product=product, user=request.user)
                response = {'success': True}
                return JsonResponse(response)


@login_required(login_url='login')
def deleteitem(request, slug):
    product = Product.objects.get(slug=slug)
    wishlist = Wishlist.objects.get(user=request.user, product=product)
    wishlist.delete()
    url = reverse_lazy('wishlist')
    messages.info(request=request, message='Item Deleted Successfully')
    return HttpResponseRedirect(url)


@login_required(login_url='login')
def delete_review(request, id):
    review = Reviews.objects.get(id=id)
    review.delete()
    messages.info(request=request, message='Review Deleted Successfully.')
    return HttpResponseRedirect(reverse_lazy('store'))


def post_review(request):
    if request.method == 'POST':
        try:
            review = request.POST['rev']
            product_id = int(request.POST['product_id'])
            product = Product.objects.get(id=product_id)
            user = request.user
            try:
                review = Reviews.objects.get(user=user, product=product)
                messages.info(request=request,
                              message='Review already exists. Delete you previous review to post new one.')
                return HttpResponseRedirect(reverse_lazy('store'))
            except:

                Reviews.objects.create(product=product, user=user, review=review)
                messages.success(request=request, message='Review successfully posted')
                return HttpResponseRedirect(reverse_lazy('store'))
        except Exception as e:
            messages.error(request=request, message='Something went wrong. Try again')
            return HttpResponseRedirect(reverse_lazy('store'))
