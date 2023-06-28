from django.contrib import admin
# Register your models here.
from baseuser.models import User

class UserAdmin(admin.ModelAdmin):
     fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','first_name', 'last_name','profile_photo','user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}))
    

admin.site.register(User)

