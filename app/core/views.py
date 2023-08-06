from django import forms
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from baseuser.models import User
from baseuser.decorators import custom_login_required,superadmin_required
from core.forms import AddSectionForm, CreateAssignmentForm, CreateClassForm,EditClassForm,AddLessonForm,EditSectionForm, StudentAssigmentForm
from. models import Classes,Notification,Assignment, StudentsAssignment
from staff.models import Lessons, Sections,Students,Teachers
from django.forms import formset_factory


# Create your views here.
@custom_login_required
def home(request):
    notifications = Notification.objects.filter(user=request.user)

    context={
        'user_details': User.objects.all(),
        'page_title':'Home',
        'notifications': notifications,
        'students': Students.objects.all().count(),
        'teachers':Teachers.objects.all().count(),
        
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
    FormSet = formset_factory(AddSectionForm, extra=1)  
    if request.method == 'POST':
        lesson_form = AddLessonForm(request.POST, prefix='lesson_form')
        section_formset = FormSet(request.POST, prefix='section_form')
        if lesson_form.is_valid() and any(form.has_changed() for form in section_formset) and all(form.is_valid() for form in section_formset):
            lesson = lesson_form.save()
            season_name = lesson_form.cleaned_data.get('season')
            lesson_title = lesson_form.cleaned_data.get('title')
            new_title = f'{lesson_title}-{season_name}'
            lesson.title = new_title
            lesson.save()
            for form in section_formset:
                if form.has_changed():
                    section = form.save()
                    section_title=form.cleaned_data.get('title')
                    new_section_title=f'{lesson_title} - {section_title}'
                    section.title=new_section_title
                    lesson.section.add(section)
                    section.save()
                    title= form.cleaned_data.get('max_student_count')
                    students=form.cleaned_data.get('students')
                    count_of_students=students.count()
            return redirect('classes')

    else:
        lesson_form = AddLessonForm(prefix='lesson_form')
        section_formset = FormSet(prefix='section_form')

    context = {
            'page_title': 'Add Lesson',
            'lesson_form': lesson_form,
            'section_formset': section_formset
        }

    return render(request, 'add_lesson.html', context)

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
    else:
        form=EditSectionForm(instance=section_data)
        context['form']=form
   
    return render(request, 'edit-section.html', context)


def add_section_view(request):
    if request.method == 'POST':
        form = AddSectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_section')  
    else:
        form = AddSectionForm()

    return render(request, 'add_section.html', {'form': form})


def lesson_list(request):
    context={
        'lessons':Lessons.objects.all()
    }
    return render(request,'lesson_list.html',context)

def lesson_detail(request,lesson_id):
    lesson=Lessons.objects.get(id=lesson_id)
    section=lesson.section.all()
    students=Students.objects.filter(students_of_section__in=section)
    initial_data={
        'lesson':lesson,
        'sender':request.user
    }
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            receiver_data=list(form.cleaned_data['receiver'])
            form.save()
            for title in receiver_data:
                section_data=Sections.objects.filter(title=title)
                for section in section_data:
                    students_of_section=section.students.all()
                    for student in students_of_section:
                        user=User.objects.get(username=student)
                        notification=Notification.objects.create(user=user,message=f'New Assigment for {lesson} ')
                        notification.save()
            return redirect(reverse('lesson-detail',args=[lesson_id]))
    else:
        form = CreateAssignmentForm(initial=initial_data)
        
  
    search_query=request.GET.get('search_query')
    if search_query:
        students=students.filter(user__first_name__icontains=search_query)
      

    context={
        'lesson':lesson,
        'section':section,
        'students':students,
        'page_title': 'Lesson Details',
        'assignment_form': form,
        'assignments': Assignment.objects.filter(lesson=lesson)
    }
    return render(request,'lesson_detail.html',context)

def assignment_detail(request, id):
    assignment = Assignment.objects.get(pk=id)
    if request.method == 'POST':
        form=StudentAssigmentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
    else:
        form=StudentAssigmentForm(initial={'assignment':assignment})
    
    context={
        'assignment': assignment,
        'form': form
        }

    return render(request, 'assignment_detail.html',context)