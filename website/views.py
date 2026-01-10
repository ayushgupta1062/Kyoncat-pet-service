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
    print(password)
    
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
    password = str(random.randint(100000, 999999))
    user = User.objects.filter(username = email).first()
    if not user:
      user = User.objects.create_user(email, "", password)

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

    request.session.pop('pending_booking', None)
    context={'config':config, 'pending':pending, 'paid': True, 'booking_id': booking.id}
    return render(request, 'website/payment.html', context)

  context={'config':config, 'pending':pending, 'paid': False}
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