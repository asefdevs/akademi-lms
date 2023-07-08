from . models import User
from django import forms
from staff.models import Student,Staff
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm,UsernameField 





class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    grade = forms.ChoiceField(
        label='Grade',
        choices=Student.GRADE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Grade'}),
        required=False,
    )

    about_teacher = forms.CharField(
        label='About Teacher',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Teacher'}),
        required=False,
    )
    position_staff=forms.ChoiceField(
        label='Position',
        choices=Staff.position_choices ,
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Position'}),
        required=False
        )
    
    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name','email', 'password','password2','user_type','gender','birthdate','country','number','profile_photo',)
        widgets={
            'username': forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}),
            'first_name': forms.TextInput(attrs={'placeholder':'FirstName','class':'form-control'}),
            'last_name': forms.TextInput(attrs={'placeholder':'LastName','class':'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder':'Email','class':'form-control'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Password','type':'password','class':'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder':'Confirm Password','type':'password'}),
            'user_type': forms.Select(attrs={'placeholder':'User Type','class':'form-control'}),
            'gender': forms.Select(attrs={'placeholder':'Gender','class':'form-control'}),
            'birthdate':forms.DateInput(attrs={'placeholder':'Birth Date','class':'form-control'}),
            'country':forms.TextInput(attrs={'placeholder':'Country','class':'form-control'}),
            'number':forms.TextInput(attrs={'placeholder':'Number','class':'form-control'}),
            'profile_photo':forms.ClearableFileInput(attrs={'placeholder':'Profile Photo','class':'form-control'}),
            
        }
    
    def clean_username(self):
        data = self.cleaned_data.get("username")
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('This username already exists')
        return data
    def clean_password(self):
        data=self.cleaned_data.get('password')
        if len(data)<8 :
            raise forms.ValidationError('password must be at least 8 characters')

        return data
    
class LoginForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username', 'password')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),
            'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),
        }

# class LoginForm( AuthenticationForm ):
#     username = UsernameField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username',"autofocus": True}))
#     password = forms.CharField(
#         widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password',"autocomplete": "current-password"}),
#     )

  



