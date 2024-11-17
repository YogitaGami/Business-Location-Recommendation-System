from django.contrib import admin
from django.urls import path
from location_recommander import views
urlpatterns = [
    path('', views.home, name='signup'),
    path('home', views.home, name='home'),
    path('signup', views.signUp_User, name='signup'),
    path('login', views.login_User, name='login'),
    path('logout', views.logout_User, name='logout'),
    path('about', views.about, name='about'),
    path('result', views.pred_result, name='result'),
    path('contact', views.contact, name='contact'),
]