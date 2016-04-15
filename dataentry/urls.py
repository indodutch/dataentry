from django.conf.urls import url

from . import views 

__author__ = "Louis Dijkstra"



# list of url patterns
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^(?P<model_str>[\w-]+)/list$', views.view_list, name='list'),
	url(r'^(?P<model_str>[\w-]+)/(?P<object_id>[0-9]+)$', views.view_detail, name='detail'),
	url(r'^files/(?P<model_str>[\w-]+)(?P<object_id>[0-9]+)/$', views.view_subset_files, name='list'),
	url(r'^drive/new/$', views.drive_new, name='drive_new'),
	url(r'^drive/(?P<pk>[0-9]+)/edit/$', views.drive_edit, name='drive_edit'),
	url(r'^sensor/new/$', views.sensor_new, name='sensor_new'),
	# url(r'^sensor/(?P<pk>[0-9]+)/edit/$', views.sensor_edit, name='sensor_edit'),
]