from django.urls import path
from core import views
from .views import submit_contact
# from .views import base_view
from .views import news_list
from django.urls import path
from .views import fetch_article_content

app_name='core'

    

urlpatterns=[
    # path('base/', base_view, name='base'),
    path('',views.news_list,name='index'),
    path('about/', views.about, name='about'),
    path('contact.html/',views.submit_contact,name='contact'),
   
    path('advertise/',views.advertise,name='advertise'),
    path('privacy/',views.privacy,name='privacy'),
    path('scrape/<str:name>', views.scrape, name="scrape"),
    
        # bookmarking
    path('bookmarks/', views.view_bookmarks, name='view_bookmarks'),

    path('remove_bookmark/<int:headline_id>/', views.remove_bookmark, name='remove_bookmark'),
    path('rate_headline/<int:headline_id>/', views.rate_headline, name='rate_headline'),

    path('top-rated/', views.top_rated_articles, name='top_rated_articles'),

# speech
    path('fetch_article_content/', fetch_article_content, name='fetch_article_content'),


]