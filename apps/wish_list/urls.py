from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
	url(r'^create$', views.create),
	url(r'^add/(?P<id>\d+)$', views.add),
	url(r'^remove/(?P<id>\d+)$', views.remove),
	url(r'^delete/(?P<id>\d+)$', views.delete),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^register$', views.register),
	url(r'^dashboard$', views.dashboard),
	url(r'^wish_items/(?P<id>\d+)$', views.display_item)
]
