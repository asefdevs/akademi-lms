from django.contrib import admin
# Register your models here.
from baseuser.models import User

class UserAdmin(admin.ModelAdmin):
     list_display = ('username', 'email', 'user_type')  # Display fields in the admin list view
     list_filter = ('user_type','gender')  # Add a filter for user_type
     fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('profile_photo','username','first_name', 'last_name','user_type','gender','birthdate','country','number')}),
       )
    

admin.site.register(User,UserAdmin)

