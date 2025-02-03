from django.shortcuts import render, redirect
from django.views import View
from store.models.product import Products
from store.models.category import Category

class ProductAddView(View):
    def get(self, request):
        categories = Category.objects.all()  # Fetch all categories
        return render(request, 'product.html', {'categories': categories})

    def post(self, request):  # POST method to handle form submissions
        postData = request.POST
        name = postData.get('name')
        price = postData.get('price')
        category_id = postData.get('category')
        uploaded_by = postData.get('uploaded_by')
        image = request.FILES.get('image')  # Handle image upload

        # Convert price to integer
        try:
            price = int(price)  # Ensure price is an integer
        except ValueError:
            price = 0  # Default to 0 if the conversion fails

        # Store form values in case of an error
        value = {
            'name': name,
            'price': price,
            'category': category_id,  # Keep this as category, matching the template
            'uploaded_by': uploaded_by
        }
        error_message = None

        # Get category object
        category = Category.objects.get(id=category_id) if category_id else None

        # Create product instance
        product = Products(
            name=name,
            price=price,
            category=category,
            uploaded_by=uploaded_by,
            image=image
        )

        # Validate product details
        error_message = self.validateProduct(product)

        if not error_message:
            product.save()  # Save the product to the database
            return redirect('homepage')  # Redirect to a product listing page (adjust as needed)
        else:
            # Ensure category is correctly passed back
            data = {
                'error': error_message,
                'values': value,  # Passing back the form values including category
                'categories': Category.objects.all()  # Pass categories back for selection
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
        return error_message
