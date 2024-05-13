from django.urls import path
from . import views

app_name='news'

urlpatterns = [
    path('scrape/<str:name>', views.scrape, name="scrape"),
    path('', views.news_list, name="home"),
]
