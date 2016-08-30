from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.router, name='router'),
    url(r'^(?P<slug>\w{10})/$', views.show, name='show'),
]
