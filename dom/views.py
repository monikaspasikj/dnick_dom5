from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import IntegrityError

from .form import ProductForm
from .models import Customer, Product, Order, OrderProduct
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse

def search_products(query):
    return Product.objects.filter(name__icontains=query)


def admin_home(request):
    # Fetch the three newest products
    newest_products = Product.objects.order_by('date_from')[:3]

    search_query = request.GET.get('search')
    if search_query:
        search_results = search_products(search_query)
        products = search_results
    else:
        products = newest_products

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            try:
                product = Product.objects.get(pk=product_id)
                product.delete()
                messages.success(request, 'Product deleted successfully.')
            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')

    context = {'products': products}
    return render(request, 'admin_home.html', context)


def user_home(request):
    newest_products = Product.objects.order_by('date_from')[:3]

    search_query = request.GET.get('search')
    if search_query:
        search_results = search_products(search_query)
        context = {'products': search_results}
    else:
        context = {'products': newest_products}

    return render(request, 'user_home.html', context)


def public_home(request):
    newest_products = Product.objects.all()[:3]

    search_query = request.GET.get('search')
    if search_query:
        search_results = search_products(search_query)
        context = {'products': search_results}
    else:
        context = {'products': newest_products}

    return render(request, 'public_home.html', context)

def custom_login(request):
    if request.method == 'POST':
        # Handle user login
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)  # Use email as username
        if user is not None:
            login(request, user)
            # Redirect to the appropriate home page based on user role
            if user.is_superuser:
                return redirect('admin_home')
            elif user.is_authenticated:
                return redirect('user_home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


def custom_register(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        surname = request.POST['surname']
        phone = request.POST['phone']
        age = int(request.POST['age'])
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['passwordConfirm']

        # Check if passwords match
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            # Try to get the user or create if it doesn't exist
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                user.set_password(password)
                user.save()

            # Create a Customer instance
            customer = Customer.objects.create(
                name=name,
                surname=surname,
                phone=phone,
                age=age,
                address=address,
                email=email,
                password=password,
                passwordConfirm=password_confirm,
                user=user,
            )

            # Redirect to the confirmation page
            return redirect('confirmation')
        except IntegrityError:
            return render(request, 'register.html', {'error': 'Email address is already registered'})

    return render(request, 'register.html')

def confirmation(request):
    return render(request, 'confirm.html')


def product_details_public(request, kod):
    product = get_object_or_404(Product, kod=kod)
    context = {'product': product}

    return render(request, 'product_details_public.html', context)

def product_details_user(request, kod):
    product = get_object_or_404(Product, kod=kod)
    context = {'product': product}

    return render(request, 'product_details.html', context)

def product_list_admin(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)  # Display 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'product_list_admin.html', context)

def product_list_user(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)  # Display 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'product_list_user.html', context)
def product_list_public(request):
    products = Product.objects.all()
    paginator = Paginator(products, 6)  # Display 6 products per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    return render(request, 'product_list_public.html', context)


# views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product


def delete_product(request, kod):
    if request.method == 'POST':
        product_item = get_object_or_404(Product, kod=kod)
        product_item.delete()
    return redirect('product_list_admin')

def about_us_public(request):
    return render(request, 'aboutus_public.html')

def about_us_user(request):
    return render(request, 'aboutus_user.html')

def about_us_admin(request):
    return render(request, 'aboutus_admin.html')

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list_admin')  # Redirect to the product list page
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})


def edit_product(request, kod):
    product = get_object_or_404(Product, kod=kod)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list_admin')
    else:
        form = ProductForm(instance=product)

    context = {'form': form, 'product': product}
    return render(request, 'edit_product.html', context)

def add_to_cart(request):
    if request.method == 'POST':
        product_kod = request.POST.get('product_kod')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, kod=product_kod)

        order, created = Order.objects.get_or_create(customer=request.user.customer)

        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)
        order_product.quantity += quantity
        order_product.save()

        return JsonResponse({'message': 'Product added to cart.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)