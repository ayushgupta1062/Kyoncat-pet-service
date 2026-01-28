import datetime
from django.conf import settings
from django.core.mail import EmailMessage
import requests
import json

from portal.models import Config

def get_current_week_days():
    today = datetime.date.today()
    
    if today.strftime('%a') == 'Sat':
        today = today + datetime.timedelta(2) 
    
    # Find the current week's starting day (Sunday)
    start_of_week = today - datetime.timedelta(days=(today.weekday() + 1) % 7)
    # Create a list of days for the current week
    week_days = [(start_of_week + datetime.timedelta(days=i)).strftime('%A, %Y-%m-%d') for i in range(7)]
    # List dates and days of the current week starting from Sunday
    week_days = [(start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
    week_day_names = [(start_of_week + datetime.timedelta(days=i)).strftime('%a') for i in range(7)]

    return zip(week_days, week_day_names)


def sendEmail(subject, body, to = None, filepath = None):
    try:
        config = Config.objects.filter(is_valid = True).first()
        settings.EMAIL_HOST = config.smtp_host
        settings.EMAIL_PORT = config.smtp_port
        settings.EMAIL_HOST_USER = config.smtp_username
        if config.smtp_host != 'smtp-relay.gmail.com':
            settings.EMAIL_HOST_PASSWORD = config.smtp_password
        settings.EMAIL_USE_TLS = True

        if to:
            to = to.split(',')
        else:
            to = config.email_to.split(',')
        
        email = EmailMessage(subject, body,from_email='{} <{}>'.format(config.name,config.smtp_username),to=to,cc=config.email_to.split(','))
        email.encoding = "utf-8"
        email.content_subtype = "html"

        if filepath != None:
            email.attach_file(filepath)

        email.send()
        
        responseJson = {'status':True, 'message': "Email send successfully."}
        return responseJson
    except Exception as e:
        responseError = {'status':False, 'message': str(e)}
        print(responseError)
        return responseError


def sendSMS(mobile, otp):
    try:
        api_key = "e2f04edd-f843-11f0-a6b2-0200cd936042"
        # Using custom OTP with 'OTP1' template to prevent Voice fallback
        url = f"https://2factor.in/API/V1/{api_key}/SMS/{mobile}/{otp}/OTP1"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"SMS Error: {e}")
        return False

def get_bulkpe_qr(amount, order_id):
    try:
        url = "https://api.bulkpe.in/client/createDynamicVpa"
        payload = json.dumps({
            "amount": amount,
            "reference_id": str(order_id)
        })
        headers = {
            'Authorization': 'Bearer aWSVQNyt+z3IiJHV+YX9UneFZtSRs1R0Yrn9gjtmn6tbpgujtLpnUCE6pmH1dGgAk3I7b49X1meRaU9Vkg+JGXdpuqmALhCS3hF4u3IzuVQfIdMFX8zcVz9CignYKfFLUJzQQjiBUPcWwa4RWu+6Tg==',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        if data.get('data') and data['data'].get('upi_uri'):
             return data['data']['upi_uri']
        return None
    except Exception as e:
        print(f"BulkPe Error: {e}")
        return None


