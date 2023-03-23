from django.contrib.auth import views as auth_views
from django.urls import path

from .views import *

urlpatterns = [
    path('register', Signup.as_view(), name='register'),
    path('login', Loginview.as_view(), name='login'),
    path('logout', logoutview, name='logout'),
    path('profile/<str:username>', Profile.as_view(), name='profile'),
    path('manage-shipping', manage_shipping, name='shipping'),
    path('delete-accounts', deleteaccount, name='deleteacc'),
    path('edit-accounts', editaccount, name='editacc'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='account/reset_password.html'),
         name='rp'),
    path('reset_password_sent',
         auth_views.PasswordResetDoneView.as_view(template_name='account/reset_password_confirm.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_password_link.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/reset_password_done.html'),
         name='password_reset_complete'),
    path('track-orders', track_order, name='trackorder'),
]
