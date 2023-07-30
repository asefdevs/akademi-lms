from django.shortcuts import  render, redirect
from baseuser.models import User
from baseuser.decorators import student_required,teacher_required,superadmin_required,custom_login_required
from staff.models import Lessons, Staff, Students,Teachers,Sections
from .forms import EditUserForm,EditTeacherForm,EditStudentForm
from django.http import JsonResponse
import json
from core.models import Classes,Settings,Seasons
from django.db.models import Q



@custom_login_required
def show_profile(request):
    user=request.user
    return render(request, 'show_profile.html',context={'user':user})

#list Views
@custom_login_required
@superadmin_required
def student_list(request):
    search_query = request.GET.get('search_query')
    filter_option = request.GET.get('filter_option')
    filter_option_class = request.GET.get('filter_option_class')
    students=Students.objects.all()
    if search_query and  filter_option_class and (filter_option == 'oldest' or filter_option == 'recent'):
            students=students.filter(
                Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query),
                class_of_students__name__icontains=filter_option_class
                )
            students=students.order_by('user__created_at' if filter_option == 'oldest' else '-user__created_at')     
    if search_query:
        students=students.filter( Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query))    
    if filter_option == 'oldest':
        students=students.order_by('user__created_at')
    if filter_option == 'recent':
        students=students.order_by('-user__created_at')
    if filter_option_class:
        students=students.filter(class_of_students__name__icontains=filter_option_class)
    context = {
        'students': students,
        'search_query': search_query ,
        'filter_option' : filter_option,
        'filter_option_class' : filter_option_class,
        'classes': Classes.objects.all(),

    }
    return render(request, 'student.html', context)

@custom_login_required
@superadmin_required
def teacher_list(request):
    search_query=request.GET.get('search_query')
    filter_option=request.GET.get('filter_option')
    teachers=Teachers.objects.all()
    if search_query and (filter_option == 'oldest' or filter_option == 'recent'):
            teachers=teachers.filter(
                Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query),
                )
            teachers=teachers.order_by('user__created_at' if filter_option == 'oldest' else '-user__created_at')        
    if search_query:
        teachers=teachers.filter(user__first_name__icontains=search_query)
    if filter_option == 'oldest':
        teachers=teachers.order_by('-user__created_at')
    if filter_option == 'recent':
        teachers=teachers.order_by('user__created_at')
    context={
        'teachers':teachers,
        'search_query':search_query,
        'filter_option':filter_option
    }
    return render(request,'teacher.html',context)

@custom_login_required
@superadmin_required
def staff_list(request):
    search_query=request.GET.get('search_query')
    filter_option=request.GET.get('filter_option')
    staff=Staff.objects.all()
    if search_query:
        staff=staff.filter(user__first_name__icontains=search_query)
    if filter_option == 'oldest':
        staff=staff.order_by('-user__created_at')
    elif filter_option == 'recent':
        staff=staff.order_by('user__created_at')
    context={
        'staff':staff,
        'search_query':search_query,
        'filter_option':filter_option
    }
    return render(request,'staff.html',context)

def error_404(request):
    return render(request,'page-error-404.html')

#edit Views

@custom_login_required
@superadmin_required
def student_edit(request,student_id):
    student = Students.objects.get(user_id=student_id) 
    user=User.objects.get(id=student_id) 
    if request.method == 'POST':  
        form_user = EditUserForm(request.POST,request.FILES, instance=user)
        form_student=EditStudentForm(request.POST, instance=student)
        if form_user.is_valid() and form_student.is_valid():
            form_user.save()
            form_student.save()
            if 'profile_photo' in request.FILES:
                 user.profile_photo = request.FILES['profile_photo']
                 user.save()
            return redirect('students')  
        else:
            {form_student: form_student}
            {form_user: form_user}
    else:
        form_user = EditUserForm(instance=user)
        form_student=EditStudentForm(instance=student)
    return render(request, 'edit-student.html', {'form_user': form_user,'form_student':form_student ,'student': student})

@custom_login_required
@superadmin_required
def teacher_edit(request,teacher_id):
    teacher=Teachers.objects.get(user_id=teacher_id) 
    user=User.objects.get(id=teacher_id) 
    if request.method == 'POST':
         form_user=EditUserForm(request.POST,request.FILES,instance=user)
         form_teacher=EditTeacherForm(request.POST,instance=teacher)
         if form_user.is_valid() and form_teacher.is_valid():
              form_user.save()
              form_teacher.save()
              if 'profile_photo' in request.FILES:
                   user.profile_photo = request.FILES['profile_photo']
                   user.save()
              return redirect('teachers')
         else:
            context={
                'form_teacher':form_teacher,
                'form_user' : form_user
                      }
            print(form_user.errors)
            print(form_teacher.errors)
        
            
    else:
        form_user = EditUserForm(instance=user)
        form_teacher=EditTeacherForm(instance=teacher)
    
    context={
         'form_user': form_user,
         'form_teacher': form_teacher,
         'teacher':teacher,
    }
    return render(request, 'teacher_edit.html', context)  

#detail Views

@custom_login_required
@student_required
def student_detail(request,student_id):
    student=Students.objects.get(user_id=student_id)
    print(student)
    active_season = str(Settings.objects.first().active_season)
    all_seasons = Seasons.objects.all()
    student_data_active = []
    student_data_past = []
    for season in all_seasons:
        lesson = Lessons.objects.filter(season__season_name=season)
        for lesson in lesson.all():
            for section in lesson.section.filter(students=student):
                data = {
                 'season_name': season.season_name,
                        }
                data['section'] = section.title
                data['teacher'] = section.teacher
                data['lesson']=lesson.title
                if season.season_name == active_season:
                    data['is_active'] = True
                    student_data_active.append(data)
                else:
                    data['is_active'] = False
                    student_data_past.append(data)

    context={
            'page_title': 'Student details',
            'student': student,
            'student_data_active': student_data_active,
            'student_data_past':student_data_past,
            'active_season':active_season,
            'classname': Classes.objects.get(student__user__username=student)
    }

    return render(request, 'student-detail.html',  context   )

@custom_login_required
@teacher_required
def teacher_detail(request,teacher_id):
     teacher=Teachers.objects.get(pk=teacher_id)
     active_season=str(Settings.objects.last())
    #  print(active_season)
     all_seasons=Seasons.objects.all()
     teacher_data_active=[]
     teacher_data_past=[]

     for season in all_seasons:
         lesson=Lessons.objects.filter(season__season_name=season)
         for lesson in lesson.all():
             for section in lesson.section.filter(teacher=teacher):
                data = {
                 'season_name': season.season_name,
                        }
                data['section'] = section.title
                data['teacher'] = section.teacher
                data['lesson']=lesson.title
                data['students']=section.students.all()
                if season.season_name == active_season:
                    data['is_active'] = True
                    teacher_data_active.append(data)
                else:

                    data['is_active'] = False
                    teacher_data_past.append(data)

             
     context={
          'teacher_data_active':teacher_data_active,
          'page_title': 'Teacher Details',
          'teacher':teacher,
          'teacher_data_past':teacher_data_past,


     }
  
     return render(request,'teacher-detail.html',context)

#delete views

@custom_login_required
@superadmin_required
def delete_student(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        try:
            student = User.objects.get(id=student_id)
            student.delete()
            return JsonResponse({'success': True, 'message': 'Student deleted successfully.'})
        except Students.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})
      

@custom_login_required
@superadmin_required
def delete_teacher(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        data = json.loads(request.body)
        teacher_id = data.get('teacher_id')
        try:
            teacher = User.objects.get(id=teacher_id)
            teacher.delete()
            return JsonResponse({'success': True, 'message': 'teacher deleted successfully.'})
        except teacher.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'teacher not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})




def test_detail(request, student_id):
    student = Students.objects.get(pk=student_id)
    active_season = str(Settings.objects.first().active_season)
    all_seasons = Seasons.objects.all()
    student_data_active = []
    student_data_past = []
    for season in all_seasons:
        lesson = Lessons.objects.filter(season__season_name=season)
        for lesson in lesson.all():
            for section in lesson.section.filter(students=student):
                data = {
                 'season_name': season.season_name,
                        }
                data['section'] = section.title
                data['teacher'] = section.teacher
                data['lesson']=lesson.title
                if season.season_name == active_season:
                    data['is_active'] = True
                    student_data_active.append(data)
                else:
                    data['is_active'] = False
                    student_data_past.append(data)

        
    return render(request, 'test_detail.html', {'student': student, 'student_data_active': student_data_active,'student_data_past':student_data_past,'active_season':active_season,})
