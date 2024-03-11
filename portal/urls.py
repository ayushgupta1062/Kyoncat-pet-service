from django.urls import path, include
from . import views, services_views

urlpatterns = [
    path('', views.signin, name="portal_signin"),
    path('signout/', views.signout, name="portal_signout"),
    path('profile/', views.profile, name="portal_profile"),
    path('password/', views.password, name="portal_password"),
    path('dashboard/', views.dashboard, name="portal_dashboard"),
    path('navigation/', views.navigation, name="portal_navigation"),
    path('navigation/add/', views.navigationAdd, name="portal_navigation_add"),
    path('navigation/<id>/edit/', views.navigationEdit, name="portal_navigation_edit"),
    path('navigation/update/', views.navigationUpdate, name="portal_navigation_update"),
    path('page/', views.page, name="portal_page"),
    path('page/add/', views.pageAdd, name="portal_page_add"),
    path('page/<id>/edit/', views.pageEdit, name="portal_page_edit"),
    
    path('s-default/', views.sDefault, name="portal_s_default"),
    path('s-default/add/', views.sDefaultAdd, name="portal_s_default_add"),
    path('s-default/<id>/edit/', views.sDefaultEdit, name="portal_s_default_edit"),
    
    path('s-html/', views.sHtml, name="portal_s_html"),
    path('s-html/add/', views.sHtmlAdd, name="portal_s_html_add"),
    path('s-html/<id>/edit/', views.sHtmlEdit, name="portal_s_html_edit"),

    path('folder/media/', views.mediaFolder, name="portal_media_folder"),
   
    path('blog/', views.blog, name="portal_blog"),
    path('blog/add/', views.blogAdd, name="portal_blog_add"),
    path('blog/<id>/edit/', views.blogEdit, name="portal_blog_edit"),
    
    path('testimoinals/', views.testimoinals, name="portal_testimoinals"),
    path('testimoinals/add/', views.testimoinalsAdd, name="portal_testimoinals_add"),
    path('testimoinals/<id>/edit/', views.testimoinalsEdit, name="portal_testimoinals_edit"),

    path('services/', services_views.services, name="portal_services"),
    path('services/add/', services_views.servicesAdd, name="portal_services_add"),
    path('services/<id>/edit/', services_views.servicesEdit, name="portal_services_edit"),
    path('services/features/', services_views.features, name="portal_features"),
    path('services/packages/', services_views.packages, name="portal_packages"),

]
