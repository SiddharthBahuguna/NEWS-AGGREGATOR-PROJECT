from django.urls import path
from core import views

app_name='core'

urlpatterns=[
    path('',views.news_list,name='index'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('advertise/',views.advertise,name='advertise'),
    path('privacy/',views.privacy,name='privacy'),
    path('scrape/<str:name>', views.scrape, name="scrape"),
]