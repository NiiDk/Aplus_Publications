from django import forms
from .models import Order, QuoteRequest

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone_number', 
            'address', 'city', 'delivery_method', 'payment_method'
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'School or Residential Address'}),
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Academic/Professional Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].required = False 

    def clean(self):
        cleaned_data = super().clean()
        delivery_method = cleaned_data.get('delivery_method')
        address = cleaned_data.get('address')
        city = cleaned_data.get('city')

        if delivery_method == Order.DeliveryMethod.DELIVERY:
            if not address or not city:
                raise forms.ValidationError("Delivery address and city are required for home/school delivery.")
        return cleaned_data

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = [
            'school_name', 'contact_person', 'email', 'phone_number',
            'address', 'academic_levels', 'subjects', 'estimated_quantity', 
            'additional_notes'
        ]
        widgets = {
            'additional_notes': forms.Textarea(attrs={'rows': 4, 'placeholder': 'E.g., Special curriculum requirements or preferred delivery dates.'}),
            'academic_levels': forms.CheckboxSelectMultiple(),
            'subjects': forms.CheckboxSelectMultiple(),
        }
