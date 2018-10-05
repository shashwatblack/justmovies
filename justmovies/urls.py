"""justmovies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from justmovies.views import HomeView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('movies', HomeView.as_view(), name='movies'),
    path('people', HomeView.as_view(), name='people'),
    path('data', HomeView.as_view(), name='data'),
    path('admin/', admin.site.urls),
    url(r'^.*$', RedirectView.as_view(url='movies', permanent=False), name='home')
]
