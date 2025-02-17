from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View

from store.models.product import Products
from store.models.orders import Order


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            quantity_ordered = cart.get(str(product.id), 0)
            if quantity_ordered > 0:
                order = Order(
                    customer=Customer(id=customer),
                    product=product,
                    price=product.price,
                    address=address,
                    phone=phone,
                    quantity=quantity_ordered
                )
                order.save()

                # Decrease product count
                product.count -= quantity_ordered
                if product.count < 0:
                    product.count = 0  # Ensure count does not go negative
                product.save()

        # Clear the cart after checkout
        request.session['cart'] = {}

        return redirect('cart')
class RemoveProduct(View):
    def get(self, request):
        request.session['cart'] = {}  # Clear all items from the cart
        return redirect('cart')  # Redirect back to cart page
