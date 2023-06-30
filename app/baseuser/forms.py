from . models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm



class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name','email', 'password','password2','user_type',)
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'FirstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'Password','type':'password'}),
            'password2': forms.TextInput(attrs={'class':'form-control','placeholder':'Confirm Password','type':'password'}),
            'user_type': forms.Select(attrs={'class':'form-control','placeholder':'User Type'}),
 
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