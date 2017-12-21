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
from django.contrib.auth import views as auth_views

from accounts import views as accounts_views
from smartAtomizer import views

urlpatterns = [
	url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^new_client', views.new_client, name='new_client'),
    url(r'^clients', views.ClientsListView.as_view(), name='clients'),
    url(r'^control_client/(?P<pk>\d+)/$', views.control_client, name='control_client'),
    url(r'^control_zone/(?P<pk>\d+)/$', views.control_zone, name='control_zone'),
    url(r'^zones/(?P<pk>\d+)/$', views.ZonesListView.as_view(), name='zones'),
    url(r'^edit_client/(?P<pk>\d+)/$', views.UpdateClientView.as_view(), name='edit_client'),
    url(r'^edit_zone/(?P<pk>\d+)/$', views.UpdateZoneView.as_view(), name='edit_zone'),
    url(r'^zones/(?P<pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/$', views.SmartAtomizerAssignedZoneView.as_view(), name='smart_atomizers_assigned_zone'),
    url(r'^new_zone/(?P<pk>\d+)/$', views.new_zone, name='new_zone'),
    url(r'^smart_atomizers', views.smart_atomizers, name='smart_atomizers'),
    url(r'^new_smart_atomizer', views.new_smart_atomizer, name='new_smart_atomizer'),
    url(r'^assign_smart_atomizer', views.assign_smart_atomizer, name='assign_smart_atomizer'),
    url(r'^admin/', admin.site.urls),
]
