from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.landingpage),
    path("customer/<slug:username>/", views.customer, name='user'),
    path("intern/<slug:username>/", views.intern, name='intern'),
    path("products", views.products),
    path("supervisor", views.supervisor, name='supervisor'),
    path("create_order/<slug:username>", views.createOrder, name='createorder'),
    path("update_order/<str:productid>/", views.updateOrder, name='updateorder'),
    path("create_intern", views.createIntern, name='createintern'),
    path("update_intern/<str:username>/", views.updateOrder, name='updateintern'),
    path("create_product", views.createProduct, name='createproduct'),
    path("update_product/<str:productid>/", views.updateProduct, name='updateproduct'),
    path("create_customer", views.createCustomer, name='createcustomer'),

]