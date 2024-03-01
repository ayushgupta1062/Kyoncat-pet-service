from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="w_index"),
    path('page/<url>/', views.page, name="w_page")
]
