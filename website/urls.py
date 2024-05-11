from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="w_index"),
    path('contact/', views.contact, name="w_contact"),
    path('booking/', views.booking, name="w_booking"),
    path('page/<url>/', views.page, name="w_page")
]
