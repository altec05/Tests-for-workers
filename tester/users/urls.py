from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name=''),
    path('home/', views.home, name='home'),
    path('landing/', views.landing_login, name='landingLogin'),

    path('login/', views.login_user, name='login'),
    path('login/reset-password', views.reset_pass, name='reset_pass'),
    path('login/password-confirmation', views.password_change_done, name='confirmation_pass'),

    path('logout/', views.logout_user, name='logout'),

    path('register/', views.register_user, name='register'),
    path('register/confirmation', views.register_confirmation, name='confirmation'),

    path('password-change/', views.change_pass, name='password_change'),
    path('password-change/done/', views.password_change_pre_done, name='password_change_done'),

    path('profile/', views.user_profile, name='my_profile'),
    path('profile/edit-profile', views.edit_profile, name='edit_profile'),
]
