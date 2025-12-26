from .cart_utils import get_or_create_cart

def cart_count(request):
    """
    Context processor to make the total items in the cart available globally.
    """
    try:
        cart = get_or_create_cart(request)
        return {'cart_total_items': cart.total_items}
    except Exception:
        return {'cart_total_items': 0}
