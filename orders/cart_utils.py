from .models import Cart, CartItem

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def merge_carts(request):
    """
    Merge guest cart into user cart upon login.
    This should be called after a successful login.
    """
    if not request.user.is_authenticated or not request.session.session_key:
        return

    session_key = request.session.session_key
    try:
        guest_cart = Cart.objects.get(session_key=session_key)
        user_cart, created = Cart.objects.get_or_create(user=request.user)

        for item in guest_cart.items.all():
            cart_item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                cart_item.quantity += item.quantity
                cart_item.save()
        
        guest_cart.delete()
    except Cart.DoesNotExist:
        pass
