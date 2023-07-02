from django.shortcuts import render, redirect,HttpResponse
from baseuser.forms import UserUpdateForm
from baseuser.decorators import student_required,teacher_required,superadmin_required
from staff.models import Lesson, Student
from .forms import EditStudentForm


@superadmin_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')
    else:
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'edit-profile.html', context)


@superadmin_required
def student_list(request):
    form = EditStudentForm()
    context = {
        'students': Student.objects.all(),
    }
    return render(request, 'student.html', context)

@superadmin_required
def student_edit(request):
    students = Student.objects.all()
    if request.method == 'POST':
        student_id = request.POST.get('student_id')  

        student = Student.objects.get(user_id=student_id)  
        form = EditStudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students')  
    else:
        form = EditStudentForm()
    return render(request, 'student-edit.html', {'students': students, 'form': form})

@student_required
def student_detail(request):
        return HttpResponse('hello guys its student detail page')

@teacher_required
def teacher_detail(request):
     context={
          'lesson':Lesson.objects.all(),
     }
     return render(request,'teacher-detail.html',context)


def error_404(request):
    return render(request,'page-error-404.html')

