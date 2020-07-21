from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm

# landing page view
# landing page for the merchants business - hardware business
# login and logout buttons and register buttons
def landingpage(request):
    return render(request, 'main/landing.html')


# customer view
# owner of a retail hardware
# only adds their credit card information once
# can (R) make purchases
# can see previous purchases
# only one who can CRUD their credit card info
# can make an order from products view

@login_required(login_url='main:login')
def customer(request, username):
    username = Customer.objects.get(name=username)
    orders = username.order_set.all()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'username': username,
        'orders': orders,
        'orders_pending': orders_pending
    }
    return render(request, 'main/orders.html', context)


# intern view
# can only see customer insensitive info
# can RU orders - change order status as delivered, cancelled, returns
@login_required(login_url='main:login')
def intern(request, username):
    username = Intern.objects.get(name=username)
    orders = Order.objects.all()
    pending_orders = orders.filter(status='Pending').count()

    context = {
        'username': username,
        'orders': orders,
        'pending_orders': pending_orders,

    }

    return render(request, 'main/intern.html', context)


# supervisor view
# supervisor can see everything
# can CRUD interns
# can CRUD products
# can CRUD customer
# can see customers insensitive info
# name,order, email, hashed creditcard info
# can delete customer
# can add customer
# send invoice to the customer
# CRU invoices - only the superuser can delete invoices
@login_required(login_url='main:login')
def supervisor(request):
    products = Product.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    interns = Intern.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    total_interns = interns.count()
    out_of_stock = products.filter(stock_number=0).count()
    pending_orders = orders.filter(status='Pending').count()
    context = {'products': products,
               'orders': orders,
               'customers': customers,
               'interns': interns,
               'total_customers': total_customers,
               'total_orders': total_orders,
               'total_interns': total_interns,
               'pending_orders': pending_orders,
               'out_of_stock': out_of_stock,
               }
    return render(request, 'main/supervisor.html', context)


# products view
# shows products and their prices and ability to place an order
@login_required(login_url='main:login')
def products(request):
    products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products})


# create order and update order form
@login_required(login_url='main:login')
def createOrder(request, username):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(name=username)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/supervisor')

    context = {'formset': formset}

    return render(request, 'main/order_form.html', context)

# create intern and update order form
@login_required(login_url='main:login')
def createIntern(request):
    form = InternForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = InternForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}

    return render(request, 'main/intern_form.html', context)

# create product and update order form
@login_required(login_url='main:login')
def createProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}

    return render(request, 'main/product_form.html', context)
@login_required(login_url='main:login')
def createCustomer(request):
    form = CustomerForm()
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}

    return render(request, 'main/customer_form.html', context)

@login_required(login_url='main:login')
def updateOrder(request, productid):
    order = Order.objects.get(id=productid)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}
    return render(request, 'main/order_form.html', context)

@login_required(login_url='main:login')
def updateIntern(request, username):
    intern = Intern.objects.get(name=username)
    form = InternForm(instance=intern)

    if request.method == 'POST':
        form = InternForm(request.POST, instance=intern)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}
    return render(request, 'main/intern_form.html', context)
@login_required(login_url='main:login')
def updateProduct(request, productid):
    product = Product.objects.get(id=productid)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'form': form}
    return render(request, 'main/product_form.html', context)

@login_required(login_url='main:login')
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('main:supervisor')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('main:login')

        context = {'form': form}
        return render(request, 'main/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('main:supervisor')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:supervisor')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'main/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('main:home')