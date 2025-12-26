from django.db import models
from django.conf import settings
from shop.models import Textbook, Subject, AcademicLevel
import uuid

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.email}"
        return f"Guest Cart - {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Textbook, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

class Order(models.Model):
    class DeliveryMethod(models.TextChoices):
        PICKUP = 'PICKUP', 'Pickup from Office'
        DELIVERY = 'DELIVERY', 'Home/School Delivery'

    class PaymentMethod(models.TextChoices):
        MOMO = 'MOMO', 'Mobile Money'
        CARD = 'CARD', 'Credit/Debit Card'
        BANK_TRANSFER = 'BANK_TRANSFER', 'Bank Transfer'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'
        PROCESSING = 'PROCESSING', 'Processing'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='orders')
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # Shipping Info
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    
    delivery_method = models.CharField(max_length=20, choices=DeliveryMethod.choices, default=DeliveryMethod.PICKUP)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.MOMO)
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    
    # Financials
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Textbook, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title if self.product else 'Deleted Product'}"

class QuoteRequest(models.Model):
    """
    Formal request for bulk or school-level textbook quotations.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        REVIEWED = 'REVIEWED', 'Under Review'
        QUOTE_SENT = 'QUOTE_SENT', 'Quote Sent'
        COMPLETED = 'COMPLETED', 'Converted to Order'
        REJECTED = 'REJECTED', 'Rejected'

    request_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # School/Entity Details
    school_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    
    # Academic Requirements
    academic_levels = models.ManyToManyField(AcademicLevel, related_name='quote_requests')
    subjects = models.ManyToManyField(Subject, related_name='quote_requests')
    estimated_quantity = models.PositiveIntegerField(help_text="Total estimated number of books required.")
    additional_notes = models.TextField(blank=True, help_text="Specific requirements or curriculum notes.")
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    admin_remarks = models.TextField(blank=True, help_text="Internal notes for processing this request.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Bulk Quote Request"
        verbose_name_plural = "Bulk Quote Requests"

    def __str__(self):
        return f"Quote Request {self.request_id} - {self.school_name}"
