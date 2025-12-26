from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'full_name', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'delivery_method', 'payment_method', 'created_at')
    search_fields = ('order_id', 'full_name', 'email', 'transaction_reference')
    readonly_fields = ('order_id', 'total_amount', 'transaction_reference', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Identification', {
            'fields': ('order_id', 'user', 'status')
        }),
        ('Customer Information', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Shipping & Delivery', {
            'fields': ('delivery_method', 'address', 'city')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'total_amount', 'transaction_reference')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def has_add_permission(self, request):
        return False # Orders should be created through checkout, not admin
