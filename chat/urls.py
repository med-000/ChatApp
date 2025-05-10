from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'),
    path('register/',views.register, name = 'register'),
    path('mypage/<str:username>/',views.mypage, name = 'mypage'),
    path('myprofile_add/<str:username>/',views.myprofile_add, name = 'myprofile_add'),
    path('home', views.home, name='home'),
    path('home/<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
] 
