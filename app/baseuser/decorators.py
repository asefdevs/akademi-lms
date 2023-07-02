from django.shortcuts import redirect

def unauthorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def student_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'student':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_permission')
    return wrapper_func


def teacher_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'teacher':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_permission')
    return wrapper_func

def superadmin_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_permission')
    return wrapper_func

                
                