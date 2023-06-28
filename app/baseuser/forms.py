from . models import User
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('username', 'first_name', 'last_name','email', 'password','user_type')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'FirstName'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'LastName'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            'password': forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
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

