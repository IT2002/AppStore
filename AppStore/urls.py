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
from django.urls import path, include

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.sit_pet, name='sit_pet'),
    path('view_pet/<str:petid>', app.views.view_pet, name='view_pet'),
    path('view_pet/interested/', app.views.interested, name='interested'),
    path('mypets/', app.views.mypets, name='mypets'),
    path('pending/', app.views.pending,  name='pending'),
    path('pending/view_offer/<str:offerid>', app.views.view_offer, name='view_offer'),
    path('pending/view_user/<str:username>', app.views.view_user, name='view_user'),
    path('history', app.views.history, name = 'history'),
    #path('', app.views.index, name='index'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit')
]
