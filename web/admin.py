from django.contrib import admin

from web.models import Chapter, Alumnum, House, Dues, Job

app_name = "web"

admin.site.register((Chapter, Alumnum, House, Dues, Job, ))
