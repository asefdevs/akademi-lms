from . models import User
from django import forms
from staff.models import Staff,Lessons
from core.models import Classes






class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
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
    classname = forms.ModelChoiceField(
        queryset=Classes.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )    
    position_teacher = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position Teacher'}),
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
            'gender': forms.Select(attrs={'placeholder':'Gender','class':'form-control'}),
            'user_type': forms.Select(attrs={'placeholder':'User Type','class':'form-control'}),
            'birthdate':forms.DateInput(attrs={'placeholder':'Birth Date','class':'form-control'}),
            'country':forms.TextInput(attrs={'placeholder':'Country','class':'form-control'}),
            'number':forms.TextInput(attrs={'placeholder':'Number','class':'form-control'}),
            'profile_photo':forms.ClearableFileInput(attrs={'placeholder':'Profile Photo','class':'form-control'}),
            
        }
    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.fields['user_type'].widget=forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data    
    
    def clean_username(self):
        data = self.cleaned_data.get("username")
        if User.objects.filter(username=data).exists():
            self.add_error('username', 'Username already exists')
        return data
    
    def clean_password(self):
        data1=self.cleaned_data.get('password')
        if len(data1)<8 :
            self.add_error('password','password must be at least 8 characters')
        return data1    
    def clean_password2(self):
        data1=self.cleaned_data.get('password')
        data2=self.cleaned_data.get('password2')
        if data1 and data2 and data1 != data2:
            self.add_error('password2','Passwords doesnt match')
        return data2


    

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}),
        }






