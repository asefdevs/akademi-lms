from django import forms
from staff.models import Student
from baseuser.models import User
from django.contrib.auth.forms import UserChangeForm























#   cag kimidi 
# class EditStudentForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.filter(user_type='student'))
#     password=None
#     class Meta:
#         model=Student
#         fields=('grade',)
#         widgets={  
#             'user':forms.Select(attrs={'class':'form-control','placeholder':'user select','name':"student_id" ,'id':"student_id"}),
#             'grade':forms.Select(attrs={'class':'form-control'}),
#         }
