import os
import requests
from flask import flash
from intasend import APIService

def convert_currency(quantity):

    url = "https://currency-converter18.p.rapidapi.com/api/v1/convert"

    querystring = {"from":"USD","to":"KES","amount":str(quantity)}

    headers = {
        "X-RapidAPI-Key": "53261179d3msh4f625af6c821a4cp17aaa5jsn475301ddb7c1",
        "X-RapidAPI-Host": "currency-converter18.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    amount = response.json()
    new_amount = round(float(amount['result']['convertedAmount']))
    
    return str(new_amount)

token = os.environ.get('INTASEND_API_TOKEN')
publishable_key = os.environ.get('INTASEND_PUBLISHABLE_KEY')

service = APIService(token=token, publishable_key=publishable_key, test=False)

def mpesa_payment(tel_number, amount):

    try:

        response = service.collect.mpesa_stk_push\
            (phone_number=int(tel_number),email=os.environ.get\
            ('GMAIL_USERNAME'),amount=int(amount),narrative="Purchase")
        
    except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return None

    return response

def payment_status(invoice_id):

    service = APIService(token=token, publishable_key=publishable_key, test=False)

    try:

        status = service.collect.status(invoice_id=str(invoice_id))

    except Exception as e:

        flash(f"Error: {str(e)}", "error")
        return None
    
    return status