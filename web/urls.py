
from django.conf.urls import url

from web import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/$', views.register, name="register"),
    url(r'^registration_done/$', views.done, name="registration_done"),
    url(r'^jobs/$', views.jobs, name="jobs"),
    url(r'^jobs/create/$', views.create_job, name="create_job_post"),
    url(r'^login/$', views.login_view, name="login"),
]

app_name = 'web'