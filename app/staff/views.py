from django.shortcuts import  render, redirect
from baseuser.models import User
from baseuser.decorators import student_required,teacher_required,superadmin_required,custom_login_required
from staff.models import Lesson, Staff, Student,Teacher
from .forms import EditUserForm,EditTeacherForm,EditStudentForm
from django.http import JsonResponse
import json
from core.models import ClassName
from django.db.models import Q



@custom_login_required
def show_profile(request):
    user=request.user
 
    return render(request, 'show_profile.html',context={'user':user})


@custom_login_required
@superadmin_required
def student_list(request):
    search_query = request.GET.get('search_query')
    filter_option = request.GET.get('filter_option')
    filter_option_class = request.GET.get('filter_option_class')
    students=Student.objects.all()
    if search_query and  filter_option_class and (filter_option == 'oldest' or filter_option == 'recent'):
        if filter_option == 'oldest':
            students=students.filter(
                Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query),
                grade__name__icontains=filter_option_class
                ).order_by('user__created_at')
        elif filter_option == 'recent':
            students=students.filter(
                Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query),
                grade__name__icontains=filter_option_class
                ).order_by('-user__created_at')
    elif search_query:
        students=students.filter( Q(user__first_name__icontains=search_query) | Q(user__last_name__icontains=search_query))    

    elif filter_option == 'oldest':
        students=students.order_by('user__created_at')
    elif filter_option == 'recent':
        students=students.order_by('-user__created_at')
    elif filter_option_class:
        students=students.filter(grade__name__icontains=filter_option_class)
    context = {
        'students': students,
        'search_query': search_query ,
        'filter_option' : filter_option,
        'filter_option_class' : filter_option_class,
        'classes': ClassName.objects.all(),
    }
    return render(request, 'student.html', context)


@custom_login_required
@superadmin_required
def student_edit(request,student_id):
    student = Student.objects.get(user_id=student_id) 
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
        form_user = EditUserForm(instance=user)
        form_student=EditStudentForm(instance=student)
    return render(request, 'edit-student.html', {'form_user': form_user,'form_student':form_student ,'student': student})


@custom_login_required
@student_required
def student_detail(request,student_id):
        context={
            'page_title': 'Student Detail',
            'student':Student.objects.get(user_id=student_id),
            'lessons':Lesson.objects.all(),
            'teachers':Teacher.objects.all(),
            'class_informations':ClassName.objects.all(),
        
        }
        return render(request, 'student-detail.html', context)


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
        except Student.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Student not found.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})




@custom_login_required
@teacher_required
def teacher_detail(request,teacher_id):
     context={
          'lesson':Lesson.objects.all(),
          'page_title': 'Teacher Detail',
          'teacher':Teacher.objects.get(user_id=teacher_id),

     }
     return render(request,'teacher-detail.html',context)

@custom_login_required
@superadmin_required
def teacher_list(request):
    search_query=request.GET.get('search_query')
    filter_option=request.GET.get('filter_option')
    teachers=Teacher.objects.all()
    if search_query:
        teachers=teachers.filter(user__first_name__icontains=search_query)
    if filter_option == 'oldest':
        teachers=teachers.order_by('-user__created_at')
    elif filter_option == 'recent':
        teachers=teachers.order_by('user__created_at')
    context={
        'teachers':teachers,
        'search_query':search_query,
        'filter_option':filter_option
    }
    return render(request,'teacher.html',context)


@custom_login_required
@superadmin_required
def teacher_edit(request,teacher_id):
    teacher=Teacher.objects.get(user_id=teacher_id) 
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
        form_user = EditUserForm(instance=user)
        form_teacher=EditTeacherForm(instance=teacher)
    
    context={
         'form_user': form_user,
         'form_teacher': form_teacher,
         'teacher':teacher,
    }
    return render(request, 'teacher_edit.html', context)        

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



