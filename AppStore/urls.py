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
#from django.contrib.auth import views as auth_views
#from django.urls import include
from django.urls import path

import app.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.home, name='home'),
    path('register/', app.views.register, name='register'),
    path('profile/<int:id>', app.views.profile, name='profile'),
    path('login/', app.views.signin, name='login'),
    path('view/<int:id>', app.views.view, name='view')
]

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index_products, name='products'),
    #path("accounts/", include("django.contrib.auth.urls")),
    #path("accounts/login/", auth_views.login().as_view, name='login'),
    #path('login/', LoginView.as_view(template_name='app/login.html'), name='login'),
    #path('', app.views.index, name='index'),
    path('add/', app.views.add, name='add'),
    #path('buy/', app.views.buy, name='buy'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
    path('login/', app.views.login, name='login'),
    path('purchase/<int:productid>', app.views.purchase, name='purchase'),
]
"""

"""
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.index, name='index'),
    path('add', app.views.add, name='add'),
    path('view/<str:id>', app.views.view, name='view'),
    path('edit/<str:id>', app.views.edit, name='edit'),
]
"""
