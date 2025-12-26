from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count
from django.utils import timezone
from orders.models import Order, QuoteRequest
from resources.models import ResourceDownload

@login_required
def user_dashboard(request):
    """
    Academic hub for students, teachers, and school admins.
    """
    user = request.user
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    recent_downloads = ResourceDownload.objects.filter(user=user).select_related('resource').order_by('-downloaded_at')[:5]
    recent_quotes = QuoteRequest.objects.filter(user=user).order_by('-created_at')[:5]
    
    context = {
        'recent_orders': recent_orders,
        'recent_downloads': recent_downloads,
        'recent_quotes': recent_quotes,
        'user_role': user.get_role_display(),
    }
    return render(request, 'dashboard/user_dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Operational overview for platform administrators.
    """
    # Sales Overview
    today = timezone.now().date()
    total_sales = Order.objects.filter(status='PAID').aggregate(total=Sum('total_amount'))['total'] or 0
    orders_today = Order.objects.filter(created_at__date=today).count()
    pending_quotes = QuoteRequest.objects.filter(status='PENDING').count()
    
    # Recent Activity
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_sales': total_sales,
        'orders_today': orders_today,
        'pending_quotes': pending_quotes,
        'recent_orders': recent_orders,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
