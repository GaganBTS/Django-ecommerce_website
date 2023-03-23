from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views import generic

from payment.forms import Shippingform
from payment.models import *
from payment.models import ShippingAddress
from .forms import *


# Create your views here.


class Signup(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('store')
    template_name = 'account/registration/signup.html'

    def form_valid(self, form):
        try:
            view = super(Signup, self).form_valid(form)
            username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(self.request, user)
            return view
        except Exception as e:
            url = reverse_lazy('register')
            messages.error(request=self.request, message=e)
            return HttpResponseRedirect(url)


class Loginview(LoginView):
    template_name = 'account/registration/login.html'
    success_url = reverse_lazy('store')


def logoutview(request):
    logout(request)
    url = reverse_lazy('store')
    messages.info(request=request, message='Logged out successfully')
    return HttpResponseRedirect(url)


class Profile(LoginRequiredMixin, View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        context = {'user': user}
        return render(request, 'account/user_profile.html', context)


@login_required(login_url='login')
def manage_shipping(request):
    try:
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        shipping = None
    form = Shippingform(instance=shipping)
    if request.method == 'POST':
        form = Shippingform(request.POST, instance=shipping)
        if form.is_valid():
            shipping_form = form.save(commit=False)
            shipping_form.user = request.user
            shipping_form.save()
            url = reverse_lazy('shipping')
            messages.info(request=request, message='Successfully updated')
            return HttpResponseRedirect(url)
    context = {'form': form}
    return render(request, 'account/shipping.html', context)


@login_required(login_url='login')
def deleteaccount(request):
    user = User.objects.get(username=request.user.username)
    user.delete()
    url = reverse_lazy('store')
    messages.info(request=request, message='Account succesfully deleted.')
    return HttpResponseRedirect(url)


@login_required(login_url='login')
def editaccount(request):
    if request.method == 'POST':
        form = Updateuserform(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            url = reverse_lazy('store')
            messages.success(request=request, message='Details Updated Successfully.')
            return HttpResponseRedirect(url)
    form = Updateuserform(instance=request.user)
    context = {'form': form}
    return render(request, 'account/profile_update.html', context)


@login_required(login_url='login')
def track_order(request):
    try:
        orders = OrderItem.objects.filter(user=request.user)
        context = {'orders': orders}
        return render(request, 'account/my_orders.html', context)
    except:
        return render(request, 'account/my_orders.html')
