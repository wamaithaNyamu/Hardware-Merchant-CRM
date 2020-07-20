from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.landingpage),
    path("customer", views.customer),
    path("intern", views.intern),
    path("products", views.products),
    path("supervisor", views.supervisor),

]