from django.shortcuts import render,redirect
from baseuser.models import User
from baseuser.decorators import custom_login_required,superadmin_required
from core.forms import CreateClassForm
from. models import ClassName

# Create your views here.
@custom_login_required
def home(request):
    
    context={
        'user_details': User.objects.all(),
        'page_title':'Home',
    }
    return render(request,'index.html',context)

@custom_login_required
@superadmin_required
def add_class(request):
    form=CreateClassForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('home')
        
    else:
        form=CreateClassForm(request.POST)

    context={
        'form': form,
    }
    return render(request,'add-class.html',context)

