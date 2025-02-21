from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.shortcuts import render
from django.contrib import messages
from django.core.files import File
from django.http.response import HttpResponse
from django.db.models import Count, Q
from datetime import date, datetime, timedelta
from portal.models import MENUTYPE, NAVIGATIONTYPE, POSITION, Blog, Booking, Config, ImageDirectory, Navigation, Pages, SectionDefault, Testimoinals
import csv
# Create your views here.

def isLogin(user):
  try:
    return user.is_staff
  except:
    return False

def signin(request):
  next = request.GET.get('next', None)
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      if user.is_staff:
        login(request, user)
        if next:
          return HttpResponseRedirect(next)
        return HttpResponseRedirect(reverse('portal_dashboard'))
      else:
        messages.error(request, 'Access denied.')  
    else:
      messages.error(
          request, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
      return HttpResponseRedirect(reverse('portal_signin'))

  context = {}
  return render(request, 'portal/signin.html', context)

def signout(request):
  logout(request)
  return HttpResponseRedirect(reverse('portal_signin'))

@user_passes_test(isLogin, login_url='portal_signin')
def profile(request):

  if request.POST:
    request.user.first_name = request.POST['first_name']
    request.user.last_name = request.POST['last_name']
    request.user.email = request.POST['email']
    request.user.save()
    
    messages.success(request, 'Updated Successfully')
    return HttpResponseRedirect(reverse('portal_profile'))

  context = {
    'nav': 'dashboard'
  }
  return render(request, 'portal/profile.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def password(request):

  if request.POST:
    
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    user = authenticate(request, username=request.user.username, password=old_password)
    if user is not None:
      user.set_password(new_password)
      user.save()
      login(request, user)
      messages.success(request, 'Updated Successfully')
    else:
      messages.warning(request, 'Password does not match.')

    return HttpResponseRedirect(reverse('portal_password'))

  context = {
    'nav': 'dashboard'
  }
  return render(request, 'portal/password.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def dashboard(request):
  today = date.today()
  week = today - timedelta(days=7)
  analytic = Booking.objects.filter(created_date__date__gte = week, created_date__date__lte = today, is_valid = True).values('created_date__date').annotate(total=Count('id')).order_by('created_date__date')
  
  label = []
  value = []
  for data in analytic:
    label.append(data['created_date__date'].strftime('%Y-%m-%d'))
    value.append(str(data['total']))
  
  count = {
    'total_booking' : Booking.objects.filter(is_valid = True).count(),
    'today_booking' : Booking.objects.filter(created_date__date = today, is_valid = True).count(),
    'today_service' : Booking.objects.filter(date = today, is_valid = True).count()
  }

  chart = {}
  if label:
    chart = {
      'label': ','.join(label),
      'value': ','.join(value)
    }
  context = {
    "nav": "dashboard",
    "chart": chart,
    "count": count
  }
  return render(request, 'portal/dashboard.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def bookings(request):
  booking = Booking.objects.filter(is_valid=True).all().order_by('-id')
  context = {
    "nav": "booking",
    "bookings":booking
  }
  return render(request, 'portal/booking.html', context)

# @user_passes_test(isLogin, login_url='portal_signin')
def bookingDetails(request):
  booking = Booking.objects.filter(id = request.GET['id'], is_valid=True).first()
  context = {
    "nav": "booking",
    "booking":booking
  }
  return render(request, 'portal/booking-details.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def navigation(request):
  if request.POST.get('formType') == 'delete':
      navigation = Navigation.objects.filter(id = request.POST['id'], is_valid = True).first()
      navigation.is_valid = False
      navigation.modified_date = request.user
      navigation.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_navigation'))
  
  navigation = Navigation.objects.filter(is_valid = True).all().order_by('type', 'priority')
  
  context = {
    "nav": "store",
    "sub_nav": "navigation",
    "navigation": navigation
  }
  return render(request, 'portal/navigation.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def navigationAdd(request):
  if request.POST:
    navigation = Navigation()
    navigation.type = request.POST['type']
    navigation.name = request.POST['name']
    navigation.menu = request.POST['menu']
    navigation.url = request.POST['url']
    navigation.title = request.POST['title']
    navigation.is_active = request.POST['is_active']
    navigation.meta_title = request.POST['meta_title']
    navigation.meta_keywords = request.POST['meta_keyword']
    navigation.meta_description = request.POST['meta_description']
    navigation.created_by = request.user
    navigation.modified_date = request.user
    navigation.level = 1
    navigation.save()
    
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_navigation_add'))

  context = {
    "nav": "store",
    "sub_nav": "navigation",
    "type": NAVIGATIONTYPE.choices(),
    "menu": MENUTYPE.choices()
  }
  return render(request, 'portal/navigation_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def navigationEdit(request,id):
  if request.POST:
    navigation = Navigation.objects.filter(id = id, is_valid = True).first()
    navigation.type = request.POST['type']
    navigation.name = request.POST['name']
    navigation.menu = request.POST['menu']
    navigation.url = request.POST['url']
    navigation.title = request.POST['title']
    navigation.is_active = request.POST['is_active']
    navigation.meta_title = request.POST['meta_title']
    navigation.meta_keywords = request.POST['meta_keyword']
    navigation.meta_description = request.POST['meta_description']
    navigation.modified_date = request.user
    navigation.save()
    
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_navigation'))
  model = Navigation.objects.filter(id = id, is_valid = True).first()
  context = {
    "nav": "store",
    "sub_nav": "navigation",
    "type": NAVIGATIONTYPE.choices(),
    "menu": MENUTYPE.choices(),
    "model":model
  }
  return render(request, 'portal/navigation_edit.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def navigationUpdate(request):
  if request.POST:
    import json
    menus = request.POST['menus']
    priority = 1
    for data in json.loads(menus):      
      if(data['item_id']):
        navigation = Navigation.objects.filter(id = data['item_id']).first()
        if navigation:
          navigation.priority = priority
          navigation.parent =  None
          if(data['parent_id']):
            navigation.parent_id = data['parent_id']
          navigation.level = data['depth']
          navigation.modified_date = request.user
          navigation.save()
          priority = priority + 1

    messages.success(request, 'Updated Successfully.')      
    return HttpResponseRedirect(reverse('portal_navigation'))

@user_passes_test(isLogin, login_url='portal_signin')
def page(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = Pages.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_page'))
  
  pages = Pages.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "page",
    "pages":pages
  }
  return render(request, 'portal/page.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def pageAdd(request):
  if request.POST:
    pages = Pages()
    pages.name = request.POST['name']
    if request.POST['navigation'] != '0':
      pages.navigation_id = request.POST['navigation']    
    pages.is_active = request.POST['is_status']
    pages.is_home = request.POST['is_home']
    pages.is_service = request.POST['is_service']
    pages.is_client = request.POST['is_client']
    pages.is_testimoinals = request.POST['is_testimoinals']
    pages.priority = request.POST['priority']
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_page_add'))
  
  navigation = Navigation.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "page",
    "navigation":navigation,
    "position": POSITION.choices()
  }
  return render(request, 'portal/page_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def pageEdit(request, id):
  page = Pages.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.name = request.POST['name']
    if request.POST['navigation'] != '0':
      page.navigation_id = request.POST['navigation']      
    page.is_active = request.POST['is_status']
    page.is_home = request.POST['is_home']
    page.is_service = request.POST['is_service']
    page.is_client = request.POST['is_client']
    page.is_testimoinals = request.POST['is_testimoinals']
    page.priority = request.POST['priority']
    page.modified_date = request.user
    page.save()

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_page'))

  navigation = Navigation.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "page",
    "page": page,
    "navigation":navigation,
    "position": POSITION.choices()
  }
  return render(request, 'portal/page_edit.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def sDefault(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = SectionDefault.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_s_default'))
  
  model = SectionDefault.objects.filter(is_valid = True, is_html = False).all()
  context = {
    "nav": "store",
    "sub_nav": "sDefault",
    "model":model
  }
  return render(request, 'portal/s_default.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def sDefaultAdd(request):
  if request.POST:
    pages = SectionDefault()
    pages.page_id = request.POST['page']
    pages.title = request.POST['title']
    pages.sub_title = request.POST['sub_title']
    pages.content = request.POST['content']
    pages.image_position = request.POST['position']
    pages.is_active = request.POST['is_status']
    pages.is_html = False
    pages.image_directory_id = request.POST['media']
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
    image = File(request.FILES.get('file', None))
    if image:
      pages.image.save(str(image), image, save=True)
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_s_default_add'))
  
  pages = Pages.objects.filter(is_active = True, is_valid = True).all()
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "sDefault",
    "pages":pages,
    "media": media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/s_default_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def sDefaultEdit(request, id):
  page = SectionDefault.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.page_id = request.POST['page']
    page.title = request.POST['title']
    page.sub_title = request.POST['sub_title']   
    page.content = request.POST['content']
    page.is_active = request.POST['is_status']
    page.image_position = request.POST['position']
    page.image_directory_id = request.POST['media']
    page.modified_date = request.user
    page.save()
    image = File(request.FILES.get('file', None))
    if image:
      page.image.save(str(image), image, save=True)

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_s_default'))

  pages = Pages.objects.filter(is_active = True, is_valid = True).all()  
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "sDefault",
    "page": page,
    "pages":pages,
    "media":media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/s_default_edit.html', context)


@user_passes_test(isLogin, login_url='portal_signin')
def sHtml(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = SectionDefault.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_s_default'))
  
  model = SectionDefault.objects.filter(is_valid = True, is_html = True).all()
  context = {
    "nav": "store",
    "sub_nav": "sHtml",
    "model":model
  }
  return render(request, 'portal/s_html.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def sHtmlAdd(request):
  if request.POST:
    pages = SectionDefault()
    pages.page_id = request.POST['page']
    pages.title = request.POST['title']
    pages.content = request.POST['content']
    pages.is_active = request.POST['is_status']
    pages.is_html = True
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_s_default_add'))
  
  pages = Pages.objects.filter(is_active = True, is_valid = True).all()
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "sHtml",
    "pages":pages,
    "media":media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/s_html_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def sHtmlEdit(request, id):
  page = SectionDefault.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.page_id = request.POST['page']
    page.title = request.POST['title']
    page.content = request.POST['content']
    page.is_active = request.POST['is_status']
    page.modified_date = request.user
    page.save()

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_s_html'))

  pages = Pages.objects.filter(is_active = True, is_valid = True).all()  
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "sHtml",
    "page": page,
    "pages":pages,
    "media":media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/s_html_edit.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def mediaFolder(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = ImageDirectory.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_media_folder'))
    
    if request.POST.get('formType') == 'add':
      pages = ImageDirectory()
      pages.name = request.POST['name']
      if(request.POST['type'] == '1'):
        pages.is_gallery = False
        pages.is_client = False
      if(request.POST['type'] == '2'):
        pages.is_gallery = False
      if(request.POST['type'] == '3'):
        pages.is_client = False
      pages.created_by = request.user
      pages.modified_date = request.user
      pages.save()
      image = File(request.FILES.get('file', None))
      if image:
        pages.image.save(str(image), image, save=True)
      messages.success(request, 'Added Successfully.')
      return HttpResponseRedirect(reverse('portal_media_folder'))
    
    if request.POST.get('formType') == 'edit':
      pages = ImageDirectory.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.name = request.POST['name']
      pages.is_client = request.POST['is_client']
      pages.is_gallery = request.POST['is_gallery']
      pages.created_by = request.user
      pages.modified_date = request.user
      pages.save()
      image = File(request.FILES.get('file', None))
      if image:
        pages.image.save(str(image), image, save=True)
      messages.success(request, 'Updated Successfully.')
      return HttpResponseRedirect(reverse('portal_media_folder'))
  
  model = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "media",
    "sub_nav": "media",
    "model":model
  }
  return render(request, 'portal/media_folder.html', context)


@user_passes_test(isLogin, login_url='portal_signin')
def blog(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = Blog.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_blog'))
  
  model = Blog.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "blog",
    "model":model
  }
  return render(request, 'portal/blog.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def blogAdd(request):
  if request.POST:
    pages = Blog()
    pages.page_id = request.POST['page']
    pages.title = request.POST['title']
    pages.sub_title = request.POST['sub_title']
    pages.content = request.POST['content']
    # pages.image_position = request.POST['position']
    pages.is_active = request.POST['is_status']
    page.is_home = request.POST['is_home']
    pages.is_html = False
    pages.image_directory_id = request.POST['media']
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
    image = File(request.FILES.get('file', None))
    if image:
      pages.image.save(str(image), image, save=True)
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_blog_add'))
  
  pages = Navigation.objects.filter(menu = MENUTYPE.BLOG, is_valid = True).all()  
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "blog",
    "pages":pages,
    "media": media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/blog_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def blogEdit(request, id):
  page = Blog.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.navigation_id = request.POST['page']
    page.title = request.POST['title']
    page.sub_title = request.POST['sub_title']   
    page.content = request.POST['content']
    page.is_active = request.POST['is_status']
    page.is_home = request.POST['is_home']
    # page.image_position = request.POST['position']
    page.image_directory_id = request.POST['media']
    page.modified_date = request.user
    page.save()
    image = File(request.FILES.get('file', None))
    if image:
      page.image.save(str(image), image, save=True)

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_blog'))

  pages = Navigation.objects.filter(menu = MENUTYPE.BLOG, is_valid = True).all()  
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "blog",
    "page": page,
    "pages":pages,
    "media":media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/blog_edit.html', context)



@user_passes_test(isLogin, login_url='portal_signin')
def testimoinals(request):
  if request.POST:
    if request.POST.get('formType') == 'delete':
      pages = Testimoinals.objects.filter(id = request.POST['id'], is_valid = True).first()
      pages.is_valid = False
      pages.modified_date = request.user
      pages.save()
      messages.success(request, 'Deleted Successfully.')
      return HttpResponseRedirect(reverse('portal_testimoinals'))
  
  model = Testimoinals.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "testimoinals",
    "model":model
  }
  return render(request, 'portal/testimoinals.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def testimoinalsAdd(request):
  if request.POST:
    pages = Testimoinals()
    pages.name = request.POST['title']
    pages.content = request.POST['content']
    pages.is_active = request.POST['is_status']
    pages.is_home = True
    pages.image_directory_id = request.POST['media']
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
    image = File(request.FILES.get('file', None))
    if image:
      pages.image.save(str(image), image, save=True)
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_testimoinals_add'))
    
  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "testimoinals",
    "media": media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/testimoinals_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def testimoinalsEdit(request, id):
  page = Testimoinals.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.name = request.POST['title']
    page.content = request.POST['content']
    page.is_active = request.POST['is_status']
    page.image_directory_id = request.POST['media']
    page.modified_date = request.user
    page.save()
    image = File(request.FILES.get('file', None))
    if image:
      page.image.save(str(image), image, save=True)

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_testimoinals'))

  media = ImageDirectory.objects.filter(is_valid = True).all()
  context = {
    "nav": "store",
    "sub_nav": "testimoinals",
    "page": page,
    "media":media,
    "position": POSITION.choices()
  }
  return render(request, 'portal/testimoinals_edit.html', context)


@user_passes_test(isLogin, login_url='portal_signin')
def config(request):
  pages = Config.objects.filter(is_valid = True).first()
  if request.POST:
    if not pages:
      pages = Config()
      
    pages.banner_title = request.POST['banner_title']
    pages.banner_sub_title = request.POST['banner_sub_title']
    pages.banner_content = request.POST['banner_content']
    pages.use_layout_two = request.POST['use_layout_two']

    pages.fb_link = request.POST['fb_link']
    pages.x_link = request.POST['x_link']
    pages.linkedin_link = request.POST['linkedin_link']
    pages.youtube_link = request.POST['youtube_link']
    pages.instagram_link = request.POST['instagram_link']
    pages.whatsapp_link = request.POST['whatsapp_link']

    pages.name = request.POST['name']
    pages.about_us = request.POST['about_us']
    pages.email = request.POST['email']
    pages.mobile = request.POST['mobile']
    pages.address = request.POST['address']
    pages.opening_hours = request.POST['opening_hours']
    pages.whatsapp_number = request.POST['whatsapp_number']
    pages.footer_script = request.POST['footer_script']

    pages.email_to = request.POST['email_to']
    pages.email_cc = request.POST['email_cc']
    pages.smtp_name = request.POST['smtp_name']
    pages.smtp_host = request.POST['smtp_host']
    pages.smtp_port = request.POST['smtp_port']
    pages.smtp_username = request.POST['smtp_username']
    pages.smtp_password = request.POST['smtp_password']
    
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()

    banner_image_one = File(request.FILES.get('banner_image_one', None))
    if banner_image_one:
      pages.banner_image_one.save(str(banner_image_one), banner_image_one, save=True)

    banner_image_two = File(request.FILES.get('banner_image_two', None))
    if banner_image_two:
      pages.banner_image_two.save(str(banner_image_two), banner_image_two, save=True)
      
    white_logo = File(request.FILES.get('white_logo', None))
    if white_logo:
      pages.white_logo.save(str(white_logo), white_logo, save=True)

    color_logo = File(request.FILES.get('color_logo', None))
    if color_logo:
      pages.color_logo.save(str(color_logo), color_logo, save=True)

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_config'))
    
  context = {
    "nav": "store",
    "sub_nav": "config",
    "pages": pages
  }
  return render(request, 'portal/config.html', context)
