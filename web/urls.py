
from django.conf.urls import url

from web import views


urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^register/$', views.register, name="register"),
    url(r'^registration_done/$', views.done, name="registration_done"),
    url(r'^jobs/$', views.jobs, name="jobs"),
    url(r'^jobs/create/$', views.create_job, name="create_job_post"),
    url(r'^login/$', views.login_view, name="login"),
    url(r'^jobs/(?P<job_id>\d+)/$', views.job_detail, name="job_detail"),
    url(r'^scholarships/$', views.scholarships, name="scholarships"), 
    url(r'^scholarship/create/$', views.create_scholarship, name="create_scholarship_post")
]

app_name = 'web'