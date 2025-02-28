from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="w_index"),
    path('contact/', views.contact, name="w_contact"),
    path('booking/', views.booking, name="w_booking"),
    path('career/', views.career, name="w_career"),
    path('signin/', views.signin, name="w_signin"),
    path('signout/', views.signout, name="w_signout"),
    path('otp/', views.otp, name="w_otp"),
    path('dashboard/', views.dashboard, name="w_dashboard"),
    path('page/<url>/', views.page, name="w_page")    
]
