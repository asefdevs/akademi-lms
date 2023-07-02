from django.contrib import admin
# Register your models here.
from baseuser.models import User

class UserAdmin(admin.ModelAdmin):
     fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('profile_photo','username','first_name', 'last_name','user_type','gender','birthdate','country','number')}),
       )
    

admin.site.register(User,UserAdmin)

