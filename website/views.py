from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from kyonkat import helper
from django.contrib.auth.models import User
from portal.models import MENUTYPE, Booking, Config, Navigation, Packages, Pages, Services
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test

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
    packages = service.packages.filter(is_valid = True).all().order_by('priorty')

    context = {'page': page, 'content':content, 'service': service, 'packages':packages, 'config':config}
    return render(request, 'website/service.html', context)
  
def contact(request):
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
    password = User.objects.make_random_password()
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
    email = request.POST['email']
    password = User.objects.make_random_password()
    user = User.objects.filter(username = email).first()
    if not user:
      user = User.objects.create_user(email, "", password)

    booking = Booking()
    booking.user = user
    booking.name = request.POST['name']
    booking.mobile = request.POST['mobile']
    booking.email = request.POST['email']
    booking.service = request.POST['service']
    booking.pet_type = request.POST['pet_type']
    booking.breed = request.POST['breed']
    booking.pet_age = request.POST['pet_age']
    booking.aggressive = request.POST['aggressive']
    booking.vaccinations = request.POST['vaccinations']
    booking.date = request.POST['date']
    booking.time = request.POST['time']
    booking.address = request.POST['address']
    booking.location_link = request.POST['location_link']
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

    messages.success(request, 'Thank you for booking, you booking Id :#{0}.'.format(booking.id))
    return HttpResponseRedirect(reverse('w_booking'))

  service = Services.objects.filter(is_valid = True).all()
  context={'service':service, 'config':config}
  return render(request, 'website/booking.html', context)
  