from django.contrib import admin

from web.models import Chapter, Alumnum, House, Dues, Job, Scholarship

app_name = "web"

def name_display(obj):
    return obj.user.get_full_name()

@admin.register(Alumnum)
class AlumnumModelAdmin(admin.ModelAdmin):
    list_display = (name_display, 'member_id', 'verified',)
    list_filter = ('profession', 'chapter', 'house', )


@admin.register(Job)
class JobModelAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'posted_by', )

admin.site.register((Chapter, House, Dues, Scholarship, ))

admin.site.site_header = "Old Saints Administration"
