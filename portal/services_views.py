from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls.base import reverse
from django.shortcuts import render
from django.contrib import messages
from django.core.files import File
from django.http.response import HttpResponse
from datetime import date, datetime, timedelta
from portal.models import MENUTYPE, NAVIGATIONTYPE, POSITION, Blog, Features, ImageDirectory, Navigation, Packages, Pages, SectionDefault, Services, Testimoinals
from portal.views import isLogin


@user_passes_test(isLogin, login_url='portal_signin')
def features(request):
  
  if request.POST:
    if request.POST.get('formType') == 'add':
      feature = Features()
      feature.name = request.POST['name']
      feature.created_by = request.user
      feature.modified_date = request.user
      feature.save()    
      messages.success(request, 'Added Successfully')

    if request.POST.get('formType') == 'update':
      feature = Features.objects.filter(id = request.POST['id']).first()
      feature.name = request.POST['name']
      feature.modified_date = request.user
      feature.save()
      messages.success(request, 'Updated Successfully')

    if request.POST.get('formType') == 'delete':
      feature = Features.objects.filter(id = request.POST['id']).first()
      feature.is_valid = False
      feature.modified_date = request.user
      feature.save()
      messages.success(request, 'Deleted Successfully')
    
    return HttpResponseRedirect(reverse('portal_features'))

  feature = Features.objects.filter(is_valid=True).all()
  context = {
    'nav': 'services',
    'sub_nav': 'features',
    'model':feature
  }
  return render(request, 'portal/services/features.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def packages(request):
  
  if request.POST:
    if request.POST.get('formType') == 'add':
      packages = Packages()
      packages.name = request.POST['name']
      packages.priorty = request.POST['priorty']
      packages.price = request.POST['price']
      packages.created_by = request.user
      packages.modified_date = request.user
      packages.save()    
      features = request.POST.getlist('features')
      packages.features.clear()
      for data in features:
          packages.features.add(data)
      messages.success(request, 'Added Successfully')

    if request.POST.get('formType') == 'update':
      packages = Packages.objects.filter(id = request.POST['id']).first()
      packages.name = request.POST['name']
      packages.priorty = request.POST['priorty']
      packages.price = request.POST['price']
      packages.modified_date = request.user
      packages.save()
      features = request.POST.getlist('features')
      packages.features.clear()
      for data in features:
          packages.features.add(data)
      messages.success(request, 'Updated Successfully')

    if request.POST.get('formType') == 'delete':
      packages = Packages.objects.filter(id = request.POST['id']).first()
      packages.is_valid = False
      packages.modified_date = request.user
      packages.save()
      messages.success(request, 'Deleted Successfully')
    
    return HttpResponseRedirect(reverse('portal_packages'))

  features = Features.objects.filter(is_valid=True).all()
  packages = Packages.objects.filter(is_valid=True).all()
  context = {
    'nav': 'services',
    'sub_nav': 'packages',
    'features':features,
    'model':packages
  }
  return render(request, 'portal/services/packages.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def services(request):
  
  if request.POST:
    if request.POST.get('formType') == 'delete':
      services = Services.objects.filter(id = request.POST['id']).first()
      services.is_valid = False
      services.modified_date = request.user
      services.save()
      messages.success(request, 'Deleted Successfully')
    
    return HttpResponseRedirect(reverse('portal_services'))

  service = Services.objects.filter(is_valid=True).all()
  context = {
    'nav': 'services',
    'sub_nav': 'services',
    'model':service
  }
  return render(request, 'portal/services/services.html', context)


@user_passes_test(isLogin, login_url='portal_signin')
def servicesAdd(request):
  if request.POST:
    pages = Services()
    pages.navigation_id = request.POST['navigation']
    pages.title = request.POST['title']
    pages.content = request.POST['content']
    pages.is_home =  request.POST['is_home']
    pages.image_directory_id = request.POST['media']
    pages.created_by = request.user
    pages.modified_date = request.user
    pages.save()
    image = File(request.FILES.get('file', None))
    if image:
      pages.image.save(str(image), image, save=True)

    packages = request.POST.getlist('packages')
    pages.packages.clear()
    for data in packages:
      pages.packages.add(data)
      
    messages.success(request, 'Added Successfully.')
    return HttpResponseRedirect(reverse('portal_services_add'))
    
  media = ImageDirectory.objects.filter(is_valid = True).all()
  packages = Packages.objects.filter(is_valid = True).all()
  navigation = Navigation.objects.filter(is_valid = True).all()
  context = {
    "nav": "services",
    "sub_nav": "services",
    "media": media,
    "packages":packages,
    "navigation":navigation
  }
  return render(request, 'portal/services/services_add.html', context)

@user_passes_test(isLogin, login_url='portal_signin')
def servicesEdit(request, id):
  page = Services.objects.filter(id = id, is_valid = True).first()
  if request.POST:
    page.navigation_id = request.POST['navigation']
    page.title = request.POST['title']
    page.content = request.POST['content']
    page.is_home = request.POST['is_home']
    page.image_directory_id = request.POST['media']
    page.created_by = request.user
    page.modified_date = request.user
    page.save()
    image = File(request.FILES.get('file', None))
    if image:
      page.image.save(str(image), image, save=True)

    packages = request.POST.getlist('packages')
    page.packages.clear()
    for data in packages:
      page.packages.add(data)

    messages.success(request, 'Updated Successfully.')
    return HttpResponseRedirect(reverse('portal_services'))

  media = ImageDirectory.objects.filter(is_valid = True).all()
  packages = Packages.objects.filter(is_valid = True).all()
  navigation = Navigation.objects.filter(is_valid = True).all()
  context = {
    "nav": "services",
    "sub_nav": "services",
    "page": page,
    "media":media,
    "packages": packages,
    "navigation":navigation
  }
  return render(request, 'portal/services/services_edit.html', context)
