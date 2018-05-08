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
from smartAtomizer import device_requests as device_requests

urlpatterns = [
	url(r'^$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),

    url(r'^dashboard', views.dashboard, name='dashboard'),

    url(r'^new_client', views.new_client, name='new_client'),
    url(r'^clients', views.ClientsListView.as_view(), name='clients'),
    url(r'^edit_client/(?P<client_pk>\d+)/$', views.UpdateClientView.as_view(), name='edit_client'),
    
    url(r'^zones/(?P<client_pk>\d+)/$', views.ZonesListView.as_view(), name='zones'),
    url(r'^zones/(?P<client_pk>\d+)/control_client/$', views.control_client, name='control_client'),
    url(r'^zones/(?P<client_pk>\d+)/edit_alerts_client/$', views.edit_alerts_client, name='edit_alerts_client'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/$', views.SmartAtomizerAssignedZoneView.as_view(), name='smart_atomizers_assigned_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/control_zone/$', views.control_zone, name='control_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/edit_alerts_zone/$', views.edit_alerts_zone, name='edit_alerts_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/edit_zone/$', views.UpdateZoneView.as_view(), name='edit_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/edit_smart_atomizer_zone/(?P<smart_atomizer_pk>\d+)/$', views.UpdateSmartAtomizerZoneView.as_view(), name='edit_smart_atomizer_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/edit_smart_atomizer_zone/(?P<smart_atomizer_pk>\d+)/edit_alerts_smart_atomizer_zone/$', views.edit_alerts_smart_atomizer_zone, name='edit_alerts_smart_atomizer_zone'),
    url(r'^zones/(?P<client_pk>\d+)/smart_atomizers_assigned_zone/(?P<zone_pk>\d+)/add_smart_atomizer_zone/$', views.add_smart_atomizer_zone, name='add_smart_atomizer_zone'),
    url(r'^new_zone/(?P<client_pk>\d+)/$', views.new_zone, name='new_zone'),

    url(r'^delete_client/(?P<client_pk>\d+)/$', views.delete_client, name='delete_client'),
    url(r'^delete_zone/(?P<zone_pk>\d+)/$', views.delete_zone, name='delete_zone'),
    url(r'^delete_smart_atomizer/(?P<smart_atomizer_pk>\d+)/$', views.delete_smart_atomizer, name='delete_smart_atomizer'),
    url(r'^delete_smart_atomizer_schedule/(?P<smart_atomizer_pk>\d+)/(?P<smart_atomizer_schedule_pk>\d+)/$', views.delete_smart_atomizer_schedule, name='delete_smart_atomizer_schedule'),
    url(r'^remove_from_zone/(?P<smart_atomizer_pk>\d+)/$', views.remove_from_zone, name='remove_from_zone'),

    url(r'^smart_atomizers', views.SmartAtomizersListView.as_view(), name='smart_atomizers'),
    url(r'^new_smart_atomizer', views.new_smart_atomizer, name='new_smart_atomizer'),

    url(r'^edit_smart_atomizer/(?P<smart_atomizer_pk>\d+)/$', views.UpdateSmartAtomizerView.as_view(), name='edit_smart_atomizer'),
    url(r'^edit_smart_atomizer/(?P<smart_atomizer_pk>\d+)/smart_atomizer_schedule/$', views.SmartAtomizerScheduleListView.as_view(), name='smart_atomizer_schedule'),
    url(r'^edit_smart_atomizer/(?P<smart_atomizer_pk>\d+)/smart_atomizer_schedule/(?P<smart_atomizer_schedule_pk>\d+)/edit_smart_atomizer_schedule/$', views.UpdateSmartAtomizerScheduleView.as_view(), name='edit_smart_atomizer_schedule'),
    url(r'^edit_smart_atomizer/(?P<smart_atomizer_pk>\d+)/new_smart_atomizer_schedule/$', views.new_smart_atomizer_schedule, name='new_smart_atomizer_schedule'),
    url(r'^pending_activations', views.PendingActivationsListView.as_view(), name='pending_activations'),
    url(r'^assign_smart_atomizer', views.assign_smart_atomizer, name='assign_smart_atomizer'),

    url(r'^alerts', views.alerts, name='alerts'),
    #url(r'^checkup', views.checkup, name='checkup'),

    url(r'^schedule', views.schedule, name='schedule'),
    url(r'^representatives', views.RepresentativesListView.as_view(), name='representatives'),
    url(r'^new_representative', views.new_representative, name='new_representative'),
    url(r'^new_checkup', views.new_checkup, name='new_checkup'),
    url(r'^reports', views.ReportsListView.as_view(), name='reports'),
    url(r'^report_checkup', views.report_checkup, name='report_checkup'),

    url(r'^admin/', admin.site.urls),

    url(r'^test_volume_log/(?P<pk>\d+)/(?P<volume>\d+)/$', device_requests.test_volume_log, name='test_volume_log'),
    url(r'^test_activation/(?P<serial>\w+)/$', device_requests.test_activation, name='test_activation'),
    url(r'^get_schedule/(?P<pk>\w+)/$', device_requests.get_schedule, name='get_schedule'),
]
