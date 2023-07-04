from . models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm
from staff.models import Student,Teacher,Lesson



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

    # teacher_role = forms.ModelChoiceField(
    #     label='Teacher Role',
    #     queryset=Lesson.objects.all(),
    #     widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Teacher Role'}),
    #     required=False,
    # )

    about_teacher = forms.CharField(
        label='About Teacher',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'About Teacher'}),
        required=False,
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
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'password'}),
        }



class UserUpdateForm(UserChangeForm):
    password=None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','email','user_type', 'gender', 'birthdate', 'country', 'number')
        widgets = {
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birth Date'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number'}),
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'FirstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'user_type': forms.Select(attrs={'class':'form-control','placeholder':'User Type'}),
        }