from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Products
from store.models.category import Category

class ProductAddView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'product.html', {'categories': categories})

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        price = postData.get('price')
        category_id = postData.get('category')
        uploaded_by = postData.get('uploaded_by')
        count = postData.get('count')
        phone_no = postData.get('phone_no')
        email = postData.get('email')
        image = request.FILES.get('image')

        # Convert price and count to integer
        try:
            price = int(price)
        except ValueError:
            price = 0

        try:
            count = int(count)
        except ValueError:
            count = 1  # Default count to 1 if invalid

        value = {
            'name': name,
            'price': price,
            'category': category_id,
            'uploaded_by': uploaded_by,
            'count': count,
            'phone_no': phone_no,
            'email': email
        }
        error_message = None

        category = Category.objects.get(id=category_id) if category_id else None

        product = Products(
            name=name,
            price=price,
            category=category,
            uploaded_by=uploaded_by,
            count=count,
            phone_no=phone_no,
            email=email,
            image=image
        )

        error_message = self.validateProduct(product)

        if not error_message:
            product.save()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value,
                'categories': Category.objects.all()
            }
            return render(request, 'product.html', data)

    def validateProduct(self, product):
        error_message = None
        if not product.name:
            error_message = "Please Enter the Product Name !!"
        elif not product.price or product.price <= 0:
            error_message = "Please Enter a valid Price for the Product"
        elif not product.category:
            error_message = "Please Select a Category for the Product"
        elif not product.uploaded_by:
            error_message = "Please Enter Your Name"
        elif not product.image:
            error_message = "Please Upload an Image for the Product"
        elif not product.count or product.count < 0:
            error_message = "Please Enter a valid Product Count"
        elif not product.phone_no:
            error_message = "Please Enter Your Phone Number"
        elif not product.email:
            error_message = "Please Enter Your Email"
        return error_message
