from django.shortcuts import render,redirect
from baseuser.models import User
from baseuser.decorators import custom_login_required
from core.forms import CreateClassForm

# Create your views here.
@custom_login_required
def home(request):
    context={
        'user_details': User.objects.all(),
    }
    return render(request,'index.html',context)


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

