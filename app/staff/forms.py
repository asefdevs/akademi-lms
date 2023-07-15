from staff.models import Student,Teacher
from baseuser.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import ClearableFileInput
from ckeditor.widgets import CKEditorWidget



class EditUserForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'gender',
            'birthdate',
            'country',
            'number',
            'profile_photo'
        )
        widgets = {
            'profile_photo': ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FirstName'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'LastName'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

# class EditStudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         fields = ('grade',)
#         widgets = {
#             'grade': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grade'}),
#         }

class EditTeacherForm(forms.ModelForm):
    class Meta:
        model=Teacher
        fields=('about_teacher', )
        widgets={
            'about_teacher': CKEditorWidget(),
        }

        


