from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'home.html')

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})
