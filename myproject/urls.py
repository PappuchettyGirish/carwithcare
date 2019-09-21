"""myproject URL Configuration

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
from django.conf.urls import url,include
from myapp import views as my_views



urlpatterns = [
    path('admin/', admin.site.urls),
    url('user/',my_views.user,name = 'user'),
    url(r'^userprofile/$',my_views.userprofile,name = 'userprofile'),
    url(r'^driver/$',my_views.driver,name = 'driver'),
    url(r'^rider/$',my_views.rider,name = 'rider'),
    url('signup/', my_views.signup, name='signup'),
    url('signupdriver/', my_views.signupdriver, name='signupdriver'),
    url('login/',my_views.login,name = 'login'),
    url('logout/',my_views.logout,name = 'logout'),
    url('logindriver/',my_views.logindriver,name = 'logindriver'),
    url('logoutdriver/',my_views.logoutdriver,name = 'logoutdriver'),
    path('', include('myapp.urls')),

]
