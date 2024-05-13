from django.urls import path
from . import views

urlpatterns = [
    path('scrape/<str:name>', views.scrape, name="scrape"),
    path('', views.news_list, name="home"),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('register/',views.Register,name='register')
]
