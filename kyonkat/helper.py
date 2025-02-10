import datetime
from django.conf import settings
from django.core.mail import EmailMessage

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

