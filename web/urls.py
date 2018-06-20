
from django.conf.urls import url

from web import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/$', views.register, name="register"),
    url(r'^registration_done/$', views.done, name="registration_done")
]

app_name = 'web'