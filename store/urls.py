from django.contrib import admin
from django.urls import path
from .views.home import Index , store
from .views.signup import Signup
from .views.login import Login , logout
from .views.cart import Cart
from .views.checkout import CheckOut, RemoveProduct
from .views.orders import OrderView
from .views.product import ProductAddView
from .middlewares.auth import  auth_middleware


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('store', store , name='store'),

    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('add_product', ProductAddView.as_view(), name='add_product'),
    path('logout', logout , name='logout'),
    path('cart', auth_middleware(Cart.as_view()) , name='cart'),
    path('check-out', CheckOut.as_view() , name='checkout'),
    path('remove-product', RemoveProduct.as_view(), name='remove_product'),  # New remove product route
    path('orders', auth_middleware(OrderView.as_view()), name='orders'),

]
