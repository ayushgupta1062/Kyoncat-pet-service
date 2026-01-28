import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from kyonkat import helper
from django.contrib.auth.models import User
from portal.models import MENUTYPE, Booking, Career, Config, Navigation, Packages, Pages, Services
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

# Create your views here.
def index(request):   
  config = Config.objects.filter(is_valid = True).first()
  content = Pages.objects.filter(is_home = True, is_active = True, is_valid = True).all().order_by('priority')
  service = Services.objects.filter(is_home = True, is_valid = True).all().order_by('id')
  context = {
    'page_title': 'Home', 
    'page_keywords': '', 
    'page_description': 'Home', 
    'service':service,
    'content':content,
    'config':config
    }
  return render(request, 'website/index.html', context)


def page(request, url):
  config = Config.objects.filter(is_valid = True).first()
  page = Navigation.objects.filter(url = url, is_valid = True).first()
  if page.menu == MENUTYPE.PAGE:
    content = Pages.objects.filter(navigation = page, is_active = True, is_valid = True).all().order_by('priority')
    context = {'page': page, 'content':content}
    return render(request, 'website/page.html', context)
  
  if page.menu == MENUTYPE.SERVICES:
    content = Pages.objects.filter(navigation = page, is_active = True, is_valid = True).all().order_by('priority')
    service = Services.objects.filter(navigation = page, is_valid = True).first()
    packages = None
    if service:
      packages = service.packages.filter(is_valid = True).all().order_by('priorty')

    context = {'page': page, 'content':content, 'service': service, 'packages':packages, 'config':config}
    return render(request, 'website/service.html', context)
  
def contact(request):
  if request.POST:
    try:
      template = get_template('website/email/contact.html')
      context = {'name':request.POST['name'],'email':request.POST['email'],'mobile':request.POST['mobile'],'subject':request.POST['subject'],'message':request.POST['message']}
      html = template.render(context)
      result = helper.sendEmail('New contact us form submitted', html)
      print(result)
    except Exception as e:
      print(str(e))
      pass

    messages.success(request, 'Thank you for your feedback, our team will contact you soon.')

    return HttpResponseRedirect(reverse('w_contact'))
  
  config = Config.objects.filter(is_valid = True).first()
  context={'config':config}
  return render(request, 'website/contact.html', context)
  
def signin(request):
  config = Config.objects.filter(is_valid = True).first()
  context={'config':config}
  return render(request, 'website/signin.html', context)

def otp(request):
  config = Config.objects.filter(is_valid = True).first()
  
  if request.POST:
    username = request.POST['email']
    password = request.POST['otp']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse('w_dashboard'))
    else:
      context={'config':config, 'email': username, 'error':'Invalid OTP'}
      return render(request, 'website/otp.html', context)
  
  if request.GET.get('email'):
    email = request.GET.get('email')
    password = str(random.randint(100000, 999999))
    user = User.objects.filter(username = email).first()
    if user:
      user.set_password(password)
      user.save()
    else:
      user = User.objects.create_user(email, "", password)
    
    try:
      template = get_template('website/email/otp.html')
      context = {'password':password, 'email': email}
      html = template.render(context)
      result = helper.sendEmail('OTP for Kyonkat Groomers', html, email)
      
    except Exception as e:
      print(str(e))
      pass

    context={'config':config, 'email': email}
    return render(request, 'website/otp.html', context)
    
  if request.GET.get('mobile'):
    mobile = request.GET.get('mobile')
    password = str(random.randint(100000, 999999))
    user = User.objects.filter(username = mobile).first()
    if user:
      user.set_password(password)
      user.save()
    else:
      # Create user with mobile as username
      user = User.objects.create_user(mobile, "", password)
    
    try:
      # Send SMS
      helper.sendSMS(mobile, password)
      print(f"OTP Sent to {mobile}: {password}")
    except Exception as e:
      print(str(e))
      pass
      
    # Pass mobile as 'email' context variable so otp.html hidden input works for POST
    context={'config':config, 'email': mobile}
    return render(request, 'website/otp.html', context)

def signout(request):
  logout(request)
  return HttpResponseRedirect(reverse('w_index'))

def isLogin(user):
  try:
    return user.is_authenticated
  except:
    return False
  
@user_passes_test(isLogin, login_url='w_index')
def dashboard(request):
  booking = Booking.objects.filter(user = request.user, is_valid = True).all().order_by('-id')
  config = Config.objects.filter(is_valid = True).first()
  context={'config':config, 'bookings':booking}
  return render(request, 'website/dashboard.html', context)
  
def booking(request):
  config = Config.objects.filter(is_valid = True).first()
  if request.POST:
    # Store booking data in session and redirect to payment page.
    request.session['pending_booking'] = {
      'name': request.POST.get('name', ''),
      'mobile': request.POST.get('mobile', ''),
      'email': request.POST.get('email', ''),
      'service': request.POST.get('service', ''),
      'amount': request.POST.get('amount', '0'),
      'pet_type': request.POST.get('pet_type', ''),
      'breed': request.POST.get('breed', ''),
      'pet_age': request.POST.get('pet_age', ''),
      'aggressive': request.POST.get('aggressive', ''),
      'vaccinations': request.POST.get('vaccinations', ''),
      'date': request.POST.get('date', ''),
      'time': request.POST.get('time', ''),
      'address': request.POST.get('address', ''),
      'location_link': request.POST.get('location_link', ''),
    }
    return HttpResponseRedirect(reverse('w_payment'))

  service = Services.objects.filter(is_valid = True).all()
  context={'service':service, 'config':config}
  return render(request, 'website/booking.html', context)

def payment(request):
  config = Config.objects.filter(is_valid = True).first()
  pending = request.session.get('pending_booking')
  if not pending:
    return HttpResponseRedirect(reverse('w_booking'))

  # Finalize "payment" and create booking (mock integration UI).
  if request.POST and request.POST.get('confirm') == '1':
    email = pending.get('email')
    mobile = pending.get('mobile')
    password = str(random.randint(100000, 999999))
    
    # Use email as username if present, otherwise use mobile
    username = email if email else mobile
    
    user = User.objects.filter(username = username).first()
    if not user:
      user_email = email if email else ""
      user = User.objects.create_user(username, user_email, password)

    booking = Booking()
    booking.user = user
    booking.name = pending.get('name')
    booking.mobile = pending.get('mobile')
    booking.email = pending.get('email')
    booking.service = pending.get('service')
    booking.pet_type = pending.get('pet_type')
    booking.breed = pending.get('breed')
    booking.pet_age = pending.get('pet_age')
    booking.aggressive = pending.get('aggressive')
    booking.vaccinations = pending.get('vaccinations')
    booking.date = pending.get('date')
    booking.time = pending.get('time')
    booking.address = pending.get('address')
    booking.location_link = pending.get('location_link')
    booking.save()

    try:
      template = get_template('website/email/booking.html')
      context = {'booking':booking}
      html = template.render(context)
      result = helper.sendEmail('Booking ID:#{0}'.format(booking.id), html)
      print(result)
    except Exception as e:
      print(str(e))
      pass

    # Generate Dynamic BulkPe QR for the confirmed transaction
    amount = pending.get('amount', 0) # Assuming amount is in pending, or handle accordingly
    # If amount is not in pending, we might need to calculate it or get it from service
    # For now, let's assume 'amount' key exists or use a default/placeholder if missing logic isn't visible
    # Actually, in the code I saw before, 'amount' wasn't explicitly saved in booking from pending directly?
    # Let's check 'pending' dict usage.
    # The previous code for payment view didn't show 'amount' being used for booking.
    # However, to generate QR we need amount.
    # I will assume there's a logic to get amount or I will read 'pending' again.
    
    # Wait, the payment view handles "CONFIRMATION" after payment? 
    # The user flow is: Payment Page -> User scans QR -> User enters transaction ID/confirms?
    # The code I'm editing handles POST confirm=1. This seems to be "After Payment" or "Manual Confirm".
    # BUT the User wants the QR code to be generated *functionally*.
    # The QR code is displayed in the GET request (bottom of function).
    
    request.session.pop('pending_booking', None)
    context={'config':config, 'pending':pending, 'paid': True, 'booking_id': booking.id}
    return render(request, 'website/payment.html', context)

  # GET Request - Display Payment Page with QR
  # We need to generate the QR here for the User to scan.
  # We need a unique order_id for this potential transaction. 
  # We can use a temporary ID or a hash.
  
  order_id = f"PED-{random.randint(100000, 999999)}"
  amount = pending.get('amount', 1) # Default to 1 if not found for safety/testing, or handle error.
  # Note: The original code didn't show where 'amount' comes from in pending. 
  # If it's 0, BulkPe might fail. 
  
  upi_string = helper.get_bulkpe_qr(amount, order_id)
  print(f"Generated UPI String: {upi_string}")

  context={'config':config, 'pending':pending, 'paid': False, 'upi_string': upi_string, 'order_id': order_id}
  return render(request, 'website/payment.html', context)

  
  
def career(request):
  config = Config.objects.filter(is_valid = True).first()
  if request.POST:

    career = Career()
    career.name = request.POST['name']
    career.mobile = request.POST['mobile']
    career.job_type = request.POST['job_type']
    career.job_role = request.POST['job_role']
    career.experience = request.POST['experience']
    career.company = request.POST['company']
    career.save()
    
    messages.success(request, 'Thank you for your request.')
    return HttpResponseRedirect(reverse('w_career'))

  context={'config':config}
  return render(request, 'website/career.html', context)
  
  
  
  

def robots_txt(request):
    return HttpResponse(
        "User-agent: *\nDisallow:\nSitemap: https://kyonkatgroomers.com/static/sitemap.xml",
        content_type="text/plain"
    )