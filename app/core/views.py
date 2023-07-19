from django.shortcuts import render,redirect
from django.urls import reverse
from baseuser.models import User
from baseuser.decorators import custom_login_required,superadmin_required
from core.forms import CreateClassForm,EditClassForm
from. models import ClassName

# Create your views here.
@custom_login_required
def home(request):
    
    context={
        'user_details': User.objects.all(),
        'page_title':'Home',
        'class_details': ClassName.objects.all(),
    }
    return render(request,'index.html',context)
def class_list(request):
    context={
        'classes':ClassName.objects.all(),
    }
    return render(request,'class_list.html',context)

@custom_login_required
@superadmin_required
def add_class(request):
    form=CreateClassForm(request.POST)
    context={
            'form': form,
            'page_title': 'Create Class'
        }    
    if request.method == 'POST':    
        class_name=request.POST.get('name')    
        if form.is_valid():
            form.save()
            return redirect(reverse('edit-class', args=[class_name]))
        else:
            context['form']=form
    else:
        form=CreateClassForm()
        context['form']=form


    return render(request,'add-class.html',context)

@custom_login_required
@superadmin_required
def edit_class(request,class_name):
    class_data=ClassName.objects.get(name=class_name)
    if request.method == 'POST':
        form=EditClassForm(request.POST,instance=class_data)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=EditClassForm(instance=class_data)
    
    context={

        'form': form,
        'class':class_data,
        'page_title': 'Edit Class'
    }
    return render (request,'edit-class.html',context)