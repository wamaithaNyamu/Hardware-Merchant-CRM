from django.shortcuts import render
from django.http import HttpResponse
from .models import *

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
def customer(request,username):
    username = Customer.objects.get(name=username)
    orders = username.order_set.all()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'username':username,
        'orders':orders,
        'orders_pending':orders_pending
    }
    return render(request, 'main/orders.html',context)

# intern view
# can only see customer insensitive info
# can RU orders - change order status as delivered, cancelled, returns
def intern(request,username):
    username = Intern.objects.get(name=username)
    orders = Order.objects.all()
    pending_orders = orders.filter(status='Pending').count()

    context= {
        'username':username,
        'orders':orders,
        'pending_orders': pending_orders,

    }

    return render(request, 'main/intern.html', context)

# supervisor view
# supervisor can see everything
# can CRUD interns
# can CRUD products
# can CRUD customer
# can see customers insensitive info
#name,order, email, hashed creditcard info
# can delete customer
# can add customer
# send invoice to the customer
# CRU invoices - only the superuser can delete invoices
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
               'orders':orders,
               'customers':customers,
               'interns': interns,
               'total_customers':  total_customers,
               'total_orders':    total_orders,
               'total_interns':total_interns,
               'pending_orders':pending_orders,
               'out_of_stock':out_of_stock,
               }
    return render(request, 'main/supervisor.html', context)


# products view
# shows products and their prices and ability to place an order
def products(request):
    products = Product.objects.all()


    return render(request, 'main/products.html',{'products':products})

# create order and update order form
def createOrder(request):

    
    context ={}

    return render(request, 'main/order_form.html',context)