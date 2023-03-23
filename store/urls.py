from django.urls import path

from .views import *

urlpatterns = [
    path('', store, name='store'),
    path('product/<slug:slug>', productinfo, name='product-info'),
    path('search/<slug:slug>', listcategory, name='list-category'),
    path('wishlist', wishlist, name='wishlist'),
    path('delete-item/<slug:slug>', deleteitem, name='del'),
    path('delete-review/<int:id>', delete_review, name='delrev'),
    path('post-review', post_review, name='postrev'),
]
