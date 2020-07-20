from django.urls import path
from . import views


app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("/customer", views.homepage, name="customer"),
    path("/hrpage", views.homepage, name="homepage"),

]