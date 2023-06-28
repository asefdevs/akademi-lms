from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate

from . forms import RegisterForm,LoginForm

# Create your views here.

def register_page (request):
    context={
        'form': RegisterForm(),
    }
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            return redirect('login')
    return render(request, 'page-register.html',context)

def login_page(request):
    context={
        'form': LoginForm(),
    }
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            context['error']='username is not good'        
    return render (request,'page-login.html',context)
    
def logout_user(request):
    logout(request)
    return redirect('login')


def error_404(request):
    return render(request,'page-error-404.html')

