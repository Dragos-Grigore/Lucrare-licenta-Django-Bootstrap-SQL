from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('success/', views.success, name='success'),
    path('log/', views.login_view, name='log'),
    path('main_page/', views.main_page, name='main_page'),
    path('human_profile/', views.human_profile, name='human_profile')



]