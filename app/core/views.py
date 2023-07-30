from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from baseuser.models import User
from baseuser.decorators import custom_login_required,superadmin_required
from core.forms import AddSectionForm, CreateClassForm,EditClassForm,AddLessonForm,EditSectionForm
from. models import Classes,Notification
from staff.models import Sections, Students

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
    class_list=Classes.objects.all()
    if search_query:
        class_list=class_list.filter(name__icontains=search_query)

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
        if form.is_valid():
            created_class=form.save()
            students=created_class.student.all()
            print(students)
            if students:
                 for student in students:
                    added_student = student.user
                    print(added_student)
                    user=User.objects.get(username=added_student)
                    message=f'You are added to {created_class.name}'
                    notification=Notification.objects.create(message=message,user=user)
                    notification.save()
                    print(notification)
                    
            return redirect('classes')
        else:
            context['form']=form    
    else:
        form=CreateClassForm()
        context['form']=form


    return render(request,'add-class.html',context)




@custom_login_required
@superadmin_required
def edit_class(request,class_name):
    class_data=Classes.objects.get(name=class_name)
    if request.method == 'POST':
        form=EditClassForm(request.POST,instance=class_data)
        if form.is_valid():
            exist_students=list(class_data.student.all())
            form.save()
            updated_students=list(class_data.student.all())
            form.save()
            for student in exist_students:
                user = User.objects.get(username=student.user)
                if student not in updated_students:
                    message = f'You are removed from {class_data} class !'
                    notification = Notification.objects.create(user=user, message=message)
                    notification.save()
            for student in updated_students:
                user=User.objects.get(username=student.user)
                if student not in exist_students:
                    old_class=Classes.objects.filter(student=student)
                    for class_ in old_class:
                        if class_.name != class_data.name:
                            class_.student.remove(student)
                            message = f'You are moved from {class_.name} to {class_data} class !'
                            break
                        else:
                            message = f'You are added to {class_data} class !'
                    notification = Notification.objects.create(user=user, message=message)
                    notification.save()
            return redirect(reverse('edit-class', args=[class_data.name]))
    else:
        form = EditClassForm(instance=class_data)    

    context={

        'form': form,
        'class':class_data,
        'page_title': 'Edit Class'
    }
    return render (request,'edit-class.html',context)

def add_lesson(request):
    form=AddLessonForm(request.POST)
    context={
        'form':form,
        'page_title': 'Add Lesson',
    }
    
    if request.method == 'POST':
        if form.is_valid():
            lesson=form.save(commit=False)
            section_title=form.cleaned_data['section']
            lesson.save()
            section=Sections.objects.filter(title=section_title).first()
            if not section:
                section=Sections.objects.create(title=section_title)
                section.save()
            else:
                lesson.section.add(section)
                lesson.save()
            return redirect(reverse('edit-section', args=[section.pk]))

    else:
        form=AddLessonForm()
        context['form']=form
       

    return render(request, 'add_lesson.html',context)


def edit_section(request, section_id):
    section_data=Sections.objects.get(pk=section_id)
    form=EditSectionForm(request.POST,instance=section_data)
    context={
        'form': form,
        'classes':Classes.objects.all(),
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            context['form']=form
            return redirect(reverse('edit-section',args=[section_id]))
        else:
            context['form']=form
            print(form.errors)
    else:
        form=EditSectionForm(instance=section_data)
        context['form']=form
   
    return render(request, 'edit-section.html', context)


def add_section_view(request):
    if request.method == 'POST':
        form = AddSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_section')  # Yeni form eklenmiş sayfaya yönlendirme
    else:
        form = AddSectionForm()

    return render(request, 'add_section.html', {'form': form})