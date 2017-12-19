"""apptoSolution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin

from smartAtomizer import views

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
    url(r'^clients', views.clients, name='clients'),
    url(r'^new_client', views.new_client, name='new_client'),
    url(r'^zones/(?P<pk>\d+)/$', views.zones, name='zones'),
    url(r'^new_zone/(?P<pk>\d+)/$', views.new_zone, name='new_zone'),
    url(r'^smart_atomizers', views.smart_atomizers, name='smart_atomizers'),
    url(r'^new_smart_atomizer', views.new_smart_atomizer, name='new_smart_atomizer'),
    url(r'^assign_smart_atomizer', views.assign_smart_atomizer, name='assign_smart_atomizer'),
    url(r'^admin/', admin.site.urls),
]
