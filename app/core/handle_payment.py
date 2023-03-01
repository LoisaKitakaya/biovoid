import os
import time
import requests
from flask import flash
from intasend import APIService

def convert_currency(quantity):

    url = "https://currency-converter-by-api-ninjas.p.rapidapi.com/v1/convertcurrency"

    querystring = {
        "have": "USD",
        "want": "KES",
        "amount": str(quantity)
    }

    headers = {
        "X-RapidAPI-Key": "53261179d3msh4f625af6c821a4cp17aaa5jsn475301ddb7c1",
        "X-RapidAPI-Host": "currency-converter-by-api-ninjas.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    amount = response.json()
    return amount['new_amount']

class MakePayment():

    def __init__(self, tel_number, amount) -> None:
        
        self.tel_number = tel_number
        self.amount = amount

        token = os.environ.get('INTASEND_API_TOKEN')
        publishable_key = os.environ.get('INTASEND_PUBLISHABLE_KEY')

        self.token = token
        self.publishable_key = publishable_key

        self.invoice_id = ''

    def mpesa_payment(self):

        service = APIService(token=self.token, publishable_key=self.publishable_key)

        try:

            response = service.collect.mpesa_stk_push\
                (phone_number=int(self.tel_number),email=os.environ.get\
                ('GMAIL_USERNAME'),amount=int(self.amount),narrative="Purchase")
            
        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return None
        
        else:

            self.invoice_id = response['invoice']['invoice_id']

        return response

    def payment_status(self):

        service = APIService(token=self.token, publishable_key=self.publishable_key)

        try:

            status = service.collect.status(invoice_id=str(self.invoice_id))

        except Exception as e:

            flash(f"Error: {str(e)}", "error")
            return None
        
        return status