from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(BaseUser)
admin.site.register(PassionUser)
admin.site.register(SuperUser)
admin.site.register(Client)
admin.site.register(Creator)
admin.site.register(UserSampleWorkTable)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Application)
admin.site.register(ProjectSampleWorkTable)
