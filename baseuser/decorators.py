from django.shortcuts import redirect,render


def custom_login_required(view_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_permission')
    return wrapper_func

def unauthorized_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def student_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'student' or request.user.user_type == 'admin' :
            return view_func(request, *args, **kwargs)
        else:
            return redirect('error_permission')
    return wrapper_func


def teacher_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.user_type == 'teacher' or request.user.user_type == 'admin':
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

                
                