from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('success/', views.success, name='success'),
    path('login/', views.login_view, name='login'),
    path('main_page/', views.main_page, name='main_page')


]