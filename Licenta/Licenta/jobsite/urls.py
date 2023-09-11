from django.urls import path
from . import views

urlpatterns = [
    path('', views.say_hello,name='hello'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log/', views.login_view, name='log'),
    path('log2FA/', views.log2FA, name='log2FA'),
    path('error_log2FA/', views.error_log2FA, name='error_log2FA'),
    path('main_page_human/', views.main_page_human, name='main_page_human'),
    path('main_page_company/', views.main_page_company, name='main_page_company'),
    path('edit_human_profile/', views.edit_human_profile, name='edit_human_profile'),
    path('edit_company_profile/', views.edit_company_profile, name='edit_company_profile'),
    path('forgot_pass/', views.forgot_pass, name='forgot_pass'),
    path('change_pass/', views.change_pass, name='change_pass'),
    path('error_change_pass/', views.error_change_pass, name='error_change_pass'),
    path('new_ad/', views.new_ad, name='new_ad'),
    path('show_filtered_ads/', views.show_filtered_ads, name='show_filtered_ads'),
    path('show_filtered_users/', views.show_filtered_users, name='show_filtered_users'),
    path('company_profile/<int:company_id>/', views.company_profile, name='company_profile'),
    path('human_profile/<int:user_id>/', views.human_profile, name='human_profile'),
    path('own_company_profile/<int:company_id>/', views.own_company_profile, name='own_company_profile'),
    path('own_human_profile/<int:user_id>/', views.own_human_profile, name='own_human_profile'),
    path('ad_page/<int:ad_id>/', views.ad_page, name='ad_page'),
    path('show_filtered_ads_not_logged/', views.show_filtered_ads_not_logged, name='show_filtered_ads_not_logged')




    


]