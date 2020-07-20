from django.shortcuts import render
from django.http import HttpResponse

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
def customer(request):
    return render(request, 'main/customer.html')

# intern view
# can only see customer insensitive info
# can RU orders - change order status as delivered, cancelled, returns
def intern(request):
    return render(request, 'main/intern.html')

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
    return render(request, 'main/supervisor.html')


# products view
# shows products and their prices and ability to place an order
def products(request):
    return render(request, 'main/products.html')
