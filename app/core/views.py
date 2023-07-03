from django.shortcuts import render,redirect
from baseuser.models import User
from baseuser.decorators import custom_login_required

# Create your views here.
@custom_login_required
def home(request):
    context={
        'user_details': User.objects.all(),
    }
    return render(request,'index.html',context)



