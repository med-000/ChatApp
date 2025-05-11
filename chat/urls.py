from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register, name = 'register'),
    path('mypage/<str:username>/',views.mypage, name = 'mypage'),
    path('myprofile_add/<str:username>/',views.myprofile_add, name = 'myprofile_add'),
    path('myprofile_edit/<str:username>/',views.myprofile_edit, name = 'myprofile_edit'),
    path('home/<str:username>/', views.home, name='home'),
    path('home/<str:username>/personal_chat_add/', views.personal_chat_add, name='personal_chat_add'),
    path('home/<str:username>/<str:nickname>-profile/', views.profile, name='profile'),
    path('home/<str:username>/<str:nickname>-profile/personal_chat_add_home', views.personal_chat_add_home, name='personal_chat_add_home'),
    path('home/<str:username>/<str:room>/', views.room, name='room'),
    path('home/<str:username>/checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
] 
