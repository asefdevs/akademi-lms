from django.shortcuts import render,redirect
from django.urls import reverse
from baseuser.models import User
from baseuser.decorators import custom_login_required,superadmin_required
from core.forms import CreateClassForm,EditClassForm,DefineTeachersForm
from. models import ClassName,Notification


# Create your views here.
@custom_login_required
def home(request):
    notifications = Notification.objects.filter(user=request.user)

    context={
        'user_details': User.objects.all(),
        'page_title':'Home',
        'notifications': notifications
    }
    return render(request,'index.html',context)


def class_list(request):
    search_query = request.GET.get('search_query')
    filter_option = request.GET.get('filter_option')
    filter_option_class = request.GET.get('filter_option_class')
    class_list=ClassName.objects.all()
    if search_query:
        class_list=class_list.filter(name__icontains=search_query)
    if filter_option == 'oldest':
        class_list=class_list.order_by('-created_at')
    elif filter_option == 'recent':
        class_list=class_list.order_by('created_at')
    if filter_option_class:
        class_list=class_list.filter(name=filter_option_class)
    
    context={
        'page_title': 'Class List',
        'class_list': class_list,
        'search_query': search_query,
        'filter_option': filter_option,
        'filter_option_class': filter_option_class,
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
            created_class=form.save()
            students=created_class.students.all()
            if students:
                 for student in students:
                    added_student = student.user.student
                    user=User.objects.get(username=added_student)
                    message=f'You are added to {created_class.name}'
                    notification=Notification.objects.create(message=message,user=user)
                    notification.save()
                    print(notification)
                    
            return redirect(reverse('define-teachers',args=[class_name]))
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
            old_students=list(class_data.students.all())
            form.save()
            updated_students=list(class_data.students.all())
            for student in old_students:
                if student not in updated_students:
                    user=User.objects.get(username=student.user.student)
                    message=f'You are removed from {class_data} class'
                    notification=Notification.objects.create(user=user, message=message)
                    notification.save()
                    student.grade=None
                    user.save()
                    print(notification.time)
            for student in updated_students:
                if student not in old_students:
                    user=User.objects.get(username=student.user.student)
                    message=f'You are added to {class_data} class'
                    notification=Notification.objects.create(user=user, message=message)
                    notification.save()
                    student.grade=class_data
                    student.save()
                    print(notification.time)                                            

            # return redirect('home')
    else:
        form=EditClassForm(instance=class_data)
    
    context={

        'form': form,
        'class':class_data,
        'page_title': 'Edit Class'
    }
    return render (request,'edit-class.html',context)

def define_teachers(request,class_name):
    class_data=ClassName.objects.get(name=class_name)
    if request.method == 'POST':
        form=DefineTeachersForm(request.POST,instance=class_data)
        if form.is_valid():
            form.save()
            return redirect('classes')
    else:
        form=DefineTeachersForm(instance=class_data)
    context={

        'form': form,
        'class':class_data,
        'page_title': 'Define Teacher for Class',
    }
    return render (request,'define_teachers.html',context)
    


