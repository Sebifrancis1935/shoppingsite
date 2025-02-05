from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        reg_no = postData.get('reg_no')  # Get registration number
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # Store form values in case of an error
        value = {
            'reg_no': reg_no,
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(
            reg_no=reg_no,  # Include registration number
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        # Validate customer details
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(reg_no, first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.reg_no:
            error_message = "Please Enter your Registration Number !!"
        elif len(customer.reg_no) < 5:
            error_message = "Registration Number must be at least 5 characters long"
        elif not customer.first_name:
            error_message = "Please Enter your First Name !!"
        elif len(customer.first_name) < 3:
            error_message = "First Name must be at least 3 characters long"
        elif not customer.last_name:
            error_message = "Please Enter your Last Name"
        elif len(customer.last_name) < 3:
            error_message = "Last Name must be at least 3 characters long"
        elif not customer.phone:
            error_message = "Enter your Phone Number"
        elif len(customer.phone) < 10:
            error_message = "Phone Number must be 10 characters long"
        elif len(customer.password) < 5:
            error_message = "Password must be at least 5 characters long"
        elif len(customer.email) < 5:
            error_message = "Email must be at least 5 characters long"
        elif customer.isExists():
            error_message = "Email Address Already Registered.."
        return error_message
