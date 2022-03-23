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
from django.urls import path

import app.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('create/user', app.views.create_user, name='create_user'),
    path('create/company', app.views.create_company, name='create_user'),
    path('job/add', app.views.add_job, name='add_job'),
    path('job/view/<str:id>', app.views.view_job, name='view_job'),
    path('job/applicants/<str:id>', app.views.view_applicants, name='view_applicants'),
    path('job/edit/<str:id>', app.views.edit_job, name='edit_job'),
]
