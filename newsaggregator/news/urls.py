from django.urls import path
from . import views

app_name='news'

urlpatterns = [
    path('scrape/<str:name>', views.scrape, name="scrape"),
    # path('', views.news_list, name="home"),
    path('bookmark/<int:headline_id>/', views.bookmark_article, name='bookmark_article'),
    path('bookmarks/', views.view_bookmarks, name='view_bookmarks'),
    path('remove_bookmark/<int:headline_id>/', views.remove_bookmark, name='remove_bookmark'),
]
