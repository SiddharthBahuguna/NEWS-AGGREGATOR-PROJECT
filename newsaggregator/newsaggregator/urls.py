from django.contrib import admin
from django.urls import path, include
from news.views import about  # Import the about view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # Include the URLs from your app
    path('about/', about, name='about'),  # Define the URL pattern for the about page

    path('user/',include('userauths.urls')),
    path('',include('core.urls')),
]
