
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
    url(r'^scholarship/create/$', views.create_scholarship, name="create_scholarship_post"),
    url(r'^find-mate/$', views.find_mate, name="find_mate",),
    url(r'^scholarships/(?P<scholarship_id>\d+)/$', views.scholarship_detail, name="scholarship_detail"),
    url(r'^about/$', views.about, name="about"),
    url('^global-executives/$', views.general_executives, name="global_executives"),
    url('^gallery/$', views.gallery, name="gallery"),
    url(r'^projects/$', views.projects, name="projects"),
    url(r'^contributions/$', views.contributions, name="contributions"),
    url(r'^dues/$', views.dues, name="dues"),
    url(r'^events/$', views.events, name="events"),
    url(r'^project/(?P<project_id>\d+)/$', views.project_detail, name="project_detail"),
    url(r'^profile/(?P<alumn_id>\d+)/$', views.profile, name="profile"),
    url(r'^logout/$', views.log_out, name="logout")
]

app_name = 'web'