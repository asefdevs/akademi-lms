from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    if  request.user.is_authenticated:
        return render(request,'index.html')
    else:
        return redirect('error_404')