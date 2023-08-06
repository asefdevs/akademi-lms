from django.contrib import admin

from core.models import Classes,Notification,Settings,Seasons,Assignment,StudentsAssignment

# Register your models here.
admin.site.register(Classes)
admin.site.register(Notification)
admin.site.register(Settings)
admin.site.register(Seasons)
admin.site.register(Assignment)
admin.site.register(StudentsAssignment)
