import os
import requests
from django.conf import settings

class PaymentGateway:
    def __init__(self):
        self.secret_key = os.getenv('PAYSTACK_SECRET_KEY')
        self.base_url = "https://api.paystack.co"

    def initialize_transaction(self, email, amount, reference):
        if not self.secret_key:
            return {"status": False, "message": "PAYSTACK_SECRET_KEY is missing in .env"}

        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": int(float(amount) * 100), # Ensure it's an integer
            "reference": reference,
            "callback_url": f"{settings.SITE_URL}/orders/payment/verify/",
        }
        
        try:
            # Added timeout to prevent "not responding" behavior
            response = requests.post(url, headers=headers, json=data, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Network Error: {str(e)}"}

    def verify_transaction(self, reference):
        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"Verification Error: {str(e)}"}
