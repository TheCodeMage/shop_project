# shop/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem


# -------------------------------
# Home Page
# -------------------------------
def home(request):
    return render(request, 'home.html')


# -------------------------------
# Shop Page - Show products and categories
# -------------------------------
def shop(request):
    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category__id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    return render(request, 'shop.html', {
        'products': products,
        'categories': categories
    })


# -------------------------------
# Product Detail Page
# -------------------------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# -------------------------------
# Add to Cart
# -------------------------------
@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop')


# -------------------------------
# Remove from Cart
# -------------------------------
@login_required
def remove_from_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(user=request.user, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('shop')


# -------------------------------
# View Cart
# -------------------------------
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
