from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse

# Create your views here.
from .forms import *
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

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
        'orders_pending': orders_pending,
    }

    return render(request, 'main/orders.html', context)



@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def sendEmail(request, username):
    username = Customer.objects.get(name=username)
    orders = username.order_set.all()
    orders_pending = orders.filter(status='Pending').count()
    cards = CreditCard.objects.all()
    # import html message.html file
    html_template = r"C:\Users\Wamaitha\Documents\SCHOOL\APT3090\CARDVAULT\apt3090\main\templates\main\invoice.html"

    context = {
        'username': username,
        'orders': orders,
        'orders_pending': orders_pending,
        'cards': cards
    }
    message = get_template('main/invoice.html').render(context)
    # html_message = get_template('main/invoice.html').render(context)
    msg = EmailMessage(
        'YOUR INVOICE',
        message,
        'achieleyemo@gmail.com',
        ['devwamaitha@gmail.com'],
    )
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    # html_message.content_subtype = 'html'  # this is required because there is no plain text email message
    # message = EmailMessage('YOUR INVOICE', html_message, 'achieleyemo@gmail.com', ['devwamaitha@gmail.com'])
    # message.send()
    print("Mail successfully sent")
    return redirect('main:supervisor')
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
@admin_only
def supervisor(request):

    products = Product.objects.all()
    orders = Order.objects.all()
    customers = Customer.objects.all()
    # interns = Intern.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    # total_interns = interns.count()
    out_of_stock = products.filter(stock_number=0).count()
    pending_orders = orders.filter(status='Pending').count()
    context = {'products': products,
               'orders': orders,
               'customers': customers,
               # 'interns': interns,
               'total_customers': total_customers,
               'total_orders': total_orders,
               # 'total_interns': total_interns,
               'pending_orders': pending_orders,
               'out_of_stock': out_of_stock,
               }
    return render(request, 'main/supervisor.html', context)


# products view
# shows products and their prices and ability to place an order
@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'main/products.html', {'products': products})


# create order and update order form
@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
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
            return redirect('main:supervisor')

    context = {'formset': formset}

    return render(request, 'main/order_form.html', context)


# create order and update order form
@login_required(login_url='main:login')
@allowed_users(allowed_roles=['customer'])
def makeOrder(request):
    curr_customer = request.user.customer
    form = OrderForm()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            the_order = form.save(commit=False)
            the_order.customer = curr_customer
            the_order.save()
            return redirect('main:user')

    context = {'forms': form}

    return render(request, 'main/make_order.html', context)



# create product and update order form
@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
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
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, productid):
    order = Order.objects.get(id=productid)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/supervisor')

    context = {'forms': form}
    return render(request, 'main/order_form.html', context)




@login_required(login_url='main:login')
@allowed_users(allowed_roles=['admin'])
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


@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
            )

            messages.success(request, 'Account was created for ' + username)

            return redirect('main:login')

    context = {'form': form}
    return render(request, 'main/register.html', context)


@unauthenticated_user
def loginPage(request):
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    #
    # print('ORDERS:', orders)

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'main/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userProfile(request):
    curr_customer = request.user.customer
    form = CustomerProfileForm(instance=curr_customer)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=curr_customer)
        if form.is_valid():
            form.save()
            return redirect('main:user')
    context = {'form': form}
    return render(request, 'main/user_profile_form.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def creditCardView(request):
    cards = CreditCard.objects.all()
    curr_customer = request.user.customer
    form = CreditCardForm(request.POST, initial={'customer': curr_customer})

    if request.method == 'POST':
        form = CreditCardForm(request.POST, instance=curr_customer)
        if form.is_valid():
            names_on_card = form.cleaned_data.get('names_on_card')
            card_number = form.cleaned_data.get('card_number')
            cvv = form.cleaned_data.get('cvv')
            expiry_month = form.cleaned_data.get('expiry_month')
            expiry_year = form.cleaned_data.get('expiry_year')

            a = CreditCard.objects.create(
                customer=curr_customer,
                names_on_card=names_on_card,
                card_number_enc=card_number,
                cvv_enc=cvv,
                expiry_month=expiry_month,
                expiry_year=expiry_year

            )
            print(a.card_number_enc)

            messages.success(request, 'Credit card details updated! ')

            return redirect('main:user')

    context = {'form': form, 'cards': cards}
    return render(request, 'main/credit_card.html', context)
