from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Textbook
from .models import Order, OrderItem, CartItem
from .cart_utils import get_or_create_cart
from .forms import CheckoutForm
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from .payment_gateways import PaymentGateway
import time

def cart_detail(request):
    cart = get_or_create_cart(request)
    return render(request, 'orders/cart_detail.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Textbook, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    if request.headers.get('HX-Request'):
        return HttpResponse(
            f'<div class="w-full bg-brandGreen text-slate-900 py-4 rounded-sm font-bold uppercase tracking-widest text-center shadow-lg flex items-center justify-center">'
            f'   <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">'
            f'       <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />'
            f'   </svg>'
            f'   Added!'
            f'</div>'
            f'<span id="cart-count" hx-swap-oob="true" class="absolute -top-2 -right-2 bg-brandBrown text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">'
            f'   {cart.total_items}'
            f'</span>'
        )
        
    messages.success(request, f"Added {product.title} to your cart.")
    return redirect('orders:cart_detail')

@require_POST
def cart_update(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
        
    if request.headers.get('HX-Request'):
        if quantity <= 0:
            return HttpResponse(status=204, headers={'HX-Trigger': 'cartUpdated'})
        
        item_total = item.product.price * item.quantity
        html = render_to_string('orders/partials/cart_summary.html', {'cart': cart})
        html += f'<span id="cart-count" hx-swap-oob="true" class="absolute -top-2 -right-2 bg-brandBrown text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">{cart.total_items}</span>'
        html += f'<td id="item-total-{item.id}" hx-swap-oob="true" class="px-6 py-6 text-right font-bold text-slate-900 italic">GHS {item_total}</td>'
        return HttpResponse(html)

    return redirect('orders:cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    
    if request.headers.get('HX-Request'):
        html = render_to_string('orders/partials/cart_summary.html', {'cart': cart})
        html += f'<span id="cart-count" hx-swap-oob="true" class="absolute -top-2 -right-2 bg-brandBrown text-white text-[10px] font-bold px-1.5 py-0.5 rounded-full">{cart.total_items}</span>'
        return HttpResponse(html)

    messages.info(request, "Item removed from cart.")
    return redirect('orders:cart_detail')

def checkout(request):
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        return redirect('shop:textbook_list')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                if request.user.is_authenticated:
                    order.user = request.user
                
                total = sum(item.product.price * item.quantity for item in cart.items.all())
                order.total_amount = total 
                order.save()
                
                for item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        price=item.product.price,
                        quantity=item.quantity
                    )
                
                cart.items.all().delete()
                return redirect('orders:initiate_payment', order_id=order.order_id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)
    
    cart_total = sum(item.product.price * item.quantity for item in cart.items.all())
    
    return render(request, 'orders/checkout.html', {
        'cart': cart, 
        'form': form,
        'cart_total': cart_total
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})

def order_detail(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, order_id=order_id)
        
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, user=request.user)
    return render(request, 'orders/invoice.html', {'order': order})

def initialize_payment(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    if order.total_amount <= 0:
        messages.error(request, "Order amount must be greater than zero.")
        return redirect('orders:order_detail', order_id=order.order_id)

    gateway = PaymentGateway()
    order.transaction_reference = f"APL-{order.order_id.hex[:8]}-{int(time.time())}"
    order.save()

    response = gateway.initialize_transaction(
        email=order.email,
        amount=order.total_amount,
        reference=order.transaction_reference
    )

    if response.get('status'):
        return redirect(response['data']['authorization_url'])
    else:
        messages.error(request, f"Payment Error: {response.get('message')}")
        return redirect('orders:order_detail', order_id=order.order_id)

def verify_payment(request):
    reference = request.GET.get('reference')
    if not reference:
        return redirect('dashboard:index')

    gateway = PaymentGateway()
    response = gateway.verify_transaction(reference)

    if response.get('status') and response['data']['status'] == 'success':
        order = get_object_or_404(Order, transaction_reference=reference)
        if order.status != Order.Status.PAID:
            order.status = Order.Status.PAID
            order.save()
        return render(request, 'orders/payment_success.html', {'order': order})
    
    messages.error(request, "Payment could not be verified.")
    return redirect('dashboard:index')
