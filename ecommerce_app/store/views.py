from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from store.models import *
from django.db import models


def index_view(request):
    objects = Category.objects.all()
    user = request.user
    username = user.username
    if  not user or user.is_anonymous:
        username = None 

    return render(request=request, template_name='index.html', context={'categories': objects, 'user': username})

def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            return render(request, 'signup.html')
        if not password:
            return render(request, 'signup.html')
        user = User(username=username)
        user.set_password(password)
        user.save()
        cart = Cart()
        cart.user = user
        cart.save()
        return render(request, 'login.html')
    else:
        return render(request, 'signup.html')

# login page
def user_login(request):
    if not request.user.is_anonymous and request.user:
        return redirect('index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username:
            return render(request, 'login.html', context={'error':"email is reuired"})
        if not password:
            return render(request, 'login.html', context={'error':"password is required"})
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)  
            
            username = user.username
            if  not user or user.is_anonymous:
                username = None 
            objects = Category.objects.all()  
            return render(request, 'index.html', context={user:username,'categories': objects}, )
        else:
            return render(request, 'login.html', context={'error':"something went wrong",})
                
    else:
        return render(request, 'login.html')

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

def products(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        return render(request, '404.html', )
    products = Product.objects.filter(category=category)
    
    # Get user's cart and cart items for checking if products are already in cart
    cart_product_ids = set()
    if request.user and not request.user.is_anonymous:
        try:
            user_cart = Cart.objects.filter(user=request.user).first()
            if user_cart:
                cart_items = CartItem.objects.filter(cart=user_cart).values_list('product_id', flat=True)
                cart_product_ids = set(cart_items)
        except Exception as e:
            print(f"Error fetching cart: {e}")
    
    return render(request, 'products.html', context={
        'products': products, 
        'category': category.name,
        'cart_product_ids': list(cart_product_ids),
        'user': request.user
    })

def search_products(request):
    search_value = request.GET.get('search')
    products = None
    if search_value:
        products = Product.objects.filter(name__icontains=search_value)
    else:
        products = Product.objects.all()    
    return render(request, 'products.html', context={'products': products, 'category':'', 'user': request.user})

@require_http_methods(["GET"])
def cart(request):
    """Display the user's shopping cart with items."""
    user = request.user
    if not user or user.is_anonymous:
        return redirect('login')
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        # If no cart exists, create an empty one for the user
        cart = Cart.objects.create(user=user, total=0)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {
        'cart': cart,
        'cartItems': cart_items,
        'user': user,
    })

def add_to_cart(request, id):
    """Add product to cart via AJAX POST request"""
    user = request.user
    
    # Check if user is authenticated
    if not user or user.is_anonymous:
        return JsonResponse({
            'success': False,
            'message': 'Please login to add items to cart',
            'redirect': '/app/login/'
        }, status=401)
    
    try:
        # Get product
        product = Product.objects.get(id=id)
        
        # Check if product already in cart
        user_cart = Cart.objects.filter(user=user).first()
        if user_cart:
            existing_item = CartItem.objects.filter(
                Q(cart=user_cart) & Q(product=product)
            ).first()
            
            if existing_item:
                return JsonResponse({
                    'success': False,
                    'message': 'Product already in cart',
                    'already_in_cart': True
                })
        
        # Get or create user's cart
        if not user_cart:
            user_cart = Cart.objects.create(user=user, total=0)
        
        # Add item to cart
        new_item = CartItem.objects.create(
            cart=user_cart,
            product=product,
            qty=1,
            amount=product.price
        )
        
        # Update cart total
        cart_items = CartItem.objects.filter(cart=user_cart)
        total = sum(item.amount for item in cart_items)
        user_cart.total = total
        user_cart.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart',
            'cart_count': CartItem.objects.filter(cart=user_cart).count(),
            'cart_total': str(user_cart.total)
        })
        
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Product not found'
        }, status=404)
    except Exception as e:
        print(f"Error adding to cart: {e}")
        return JsonResponse({
            'success': False,
            'message': 'Error adding product to cart'
        }, status=500)

@require_http_methods(["GET", "POST"])
def checkout(request):
    """Render checkout form (GET) and process order placement (POST)."""
    user = request.user
    if not user or user.is_anonymous:
        return redirect('login')
    cart = Cart.objects.filter(user=user).first()
    if not cart:
        return redirect('cart')
    cart_items = CartItem.objects.filter(cart=cart)
    if request.method == 'POST':
        address = request.POST.get('address', '').strip()
        phone = request.POST.get('phone', '').strip()
        payment_method = request.POST.get('payment_method', 'COD')
        # Create order with extra details
        order = Order.objects.create(
            user=user,
            total_price=cart.total,
            address=address,
            phone=phone,
            payment_method=payment_method,
        )
        # Create order items from cart items
        OrderItem.objects.bulk_create([
            OrderItem(
                product=item.product,
                order=order,
                qty=item.qty,
                price=item.amount,
            ) for item in cart_items
        ])
        # Clear cart
        cart.delete()
        # Redirect to orders page
        return redirect('orders')
    # GET request – render checkout page
    return render(request, 'checkout.html', {
        'cart': cart,
        'cart_items': cart_items,
    })


def orders(request):
    """Display a list of the user's past orders with their items."""
    user = request.user
    if not user or user.is_anonymous:
        return redirect('login')
    # Get all orders for the user, most recent first
    user_orders = Order.objects.filter(user=user).order_by('-id')
    # Prefetch related items for efficiency
    user_orders = user_orders.prefetch_related('orderitem_set')
    return render(request, 'orders.html', context={'orders': user_orders, 'user': user})

def delete_cart_item(request, id):
    """Remove an item from the user's cart and recalculate total."""
    try:
        item = CartItem.objects.get(id=id)
        cart = Cart.objects.get(id=item.cart.id)
        # Delete the item first
        item.delete()
        # Recalculate cart total from remaining items
        remaining_items = CartItem.objects.filter(cart=cart)
        cart.total = sum(ci.amount for ci in remaining_items)
        cart.save()
    except CartItem.DoesNotExist:
        return render(request, '404.html', )
    # Redirect back to the cart page
    return redirect('cart')

def increment(request, id):
    """Increase quantity of a cart item and recalculate totals."""
    try:
        item = CartItem.objects.get(id=id)
        # increase quantity
        item.qty += 1
        # update amount (price * qty)
        item.amount = item.qty * item.product.price
        item.save()
        # recalculate cart total from all items
        cart = Cart.objects.get(id=item.cart.id)
        cart_total = CartItem.objects.filter(cart=cart).aggregate(total=models.Sum('amount'))['total'] or 0
        cart.total = cart_total
        cart.save()
    except CartItem.DoesNotExist:
        return render(request, '404.html', )
    return redirect('cart')

def decrement(request, id):
    """Decrease quantity of a cart item, remove if qty reaches 0, and recalculate totals."""
    try:
        item = CartItem.objects.get(id=id)
        if item.qty <= 1:
            # Remove the item entirely
            cart = Cart.objects.get(id=item.cart.id)
            item.delete()
        else:
            # Decrease quantity and update amount
            item.qty -= 1
            item.amount = item.qty * item.product.price
            item.save()
            cart = Cart.objects.get(id=item.cart.id)
        # Recalculate cart total from remaining items
        cart_total = CartItem.objects.filter(cart=cart).aggregate(total=models.Sum('amount'))['total'] or 0
        cart.total = cart_total
        cart.save()
    except CartItem.DoesNotExist:
        return render(request, '404.html', )
    return redirect('cart')
