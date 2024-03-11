from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls.base import reverse
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from portal.models import MENUTYPE, Navigation, Packages, Pages, Services

# Create your views here.
def index(request): 
  content = Pages.objects.filter(is_home = True, is_active = True, is_valid = True).all().order_by('priority')
  service = Services.objects.filter(is_home = True, is_valid = True).all().order_by('id')
  context = {
    'page_title': 'Home', 
    'page_keywords': '', 
    'page_description': 'Home', 
    'service':service,
    'content':content
    }
  return render(request, 'website/index.html', context)


def page(request, url):
  page = Navigation.objects.filter(url = url, is_valid = True).first()
  if page.menu == MENUTYPE.PAGE:
    content = Pages.objects.filter(navigation = page, is_active = True, is_valid = True).all().order_by('priority')
    context = {'page': page, 'content':content}
    return render(request, 'website/page.html', context)
  
  if page.menu == MENUTYPE.SERVICES:
    content = Pages.objects.filter(navigation = page, is_active = True, is_valid = True).all().order_by('priority')
    service = Services.objects.filter(navigation = page, is_valid = True).first()
    packages = service.packages.filter(is_valid = True).all().order_by('priorty')

    context = {'page': page, 'content':content, 'service': service, 'packages':packages}
    return render(request, 'website/service.html', context)
  