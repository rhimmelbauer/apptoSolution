from django.contrib import admin
from .models import *



admin.site.register(Client)
admin.site.register(Zone)
admin.site.register(SmartAtomizer)
admin.site.register(ErrorLog)
admin.site.register(Alert)
admin.site.register(VolumeLog)
admin.site.register(SyncLog)
admin.site.register(CheckUp)
admin.site.register(Representative)
admin.site.register(Report)
admin.site.register(SmartAtomizerSchedule)