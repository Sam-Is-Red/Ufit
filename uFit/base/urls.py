from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [path("", views.welcomePage, name="hello"),
               path("privacy/", views.privacyPage, name="privacy"),
               path("home/", views.homePage, name="home"),
               path("registrationpage/", views.registration_page, name="registrationpage"),
               path("chatpage/", views.chatpage, name="chatpage"),
               path("postpage/", views.postpage, name="postpage"),
               path("profilepage/", views.profilepage, name="profilepage"),
               path("loginpage/", views.login_page, name="loginpage"),
               path('loginpage/', auth_views.LoginView.as_view(), name='loginpage'),
               path('logout/', auth_views.LogoutView.as_view(), name='logout'),]


