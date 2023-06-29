from django.contrib import admin
# Register your models here.
from baseuser.models import User

class UserAdmin(admin.ModelAdmin):
     fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name', 'last_name','profile_photo','user_type','gender','country','birthday','about','grade')}),
       )
    

admin.site.register(User,UserAdmin)

