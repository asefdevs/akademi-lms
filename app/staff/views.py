from django.shortcuts import render, redirect,HttpResponse
from baseuser.models import User
from baseuser.decorators import student_required,teacher_required,superadmin_required,custom_login_required
from staff.models import Lesson, Student,Teacher
from .forms import EditStudentForm,EditUserForm,EditTeacherForm



@custom_login_required
@superadmin_required
def student_list(request):
    context = {
        'students': Student.objects.all(),
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
        
        }
        return render(request, 'student-detail.html', context)


@custom_login_required
@teacher_required
def teacher_detail(request,teacher_id):
     context={
          'lesson':Lesson.objects.all(),
          'page_title': 'Teacher Detail',
          'teacher':Teacher.objects.get(user_id=teacher_id)

     }
     return render(request,'teacher-detail.html',context)

@custom_login_required
@superadmin_required
def teacher_list(request):
    context={
        'teachers':Teacher.objects.all(),
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
         'teacher':teacher
    }
    return render(request, 'teacher_edit.html', context)        



def error_404(request):
    return render(request,'page-error-404.html')



