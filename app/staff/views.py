from django.shortcuts import render, redirect,HttpResponse
from baseuser.forms import UserUpdateForm
from baseuser.decorators import student_required,teacher_required,unauthorized_user,superadmin_required
from staff.models import Lesson

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

