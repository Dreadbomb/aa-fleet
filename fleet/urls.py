from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'fleet'

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
     url(r'^create/$', views.create_fleet, name='create_fleet'),
     url(r'^save/$', views.save_fleet, name='save_fleet'),
     url(r'^join/(?P<fleet_id>[0-9]+)$', views.join_fleet, name='join_fleet')
]