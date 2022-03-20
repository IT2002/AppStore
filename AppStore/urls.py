"""AppStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path


import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appstore_admin', app.views.appstore_admin, name='appstore_admin'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('', app.views.index, name='index'),
    re_path(r'^listing/(?:(?P<id>\w+)/)?$', app.views.listing, name='listing'),
    # re_path(r'^listing/(?:mode-(?P<mode>\d+)/)?$',  app.views.listing, name = 'listing'),
    # path('listing/<str:id>', app.views.listing, name = 'listing'),
    path('add_listing', app.views.add_listing, name='add_listing'),
    path('view_listing/<str:id>', app.views.view_listing, name='view_listing'),
]
