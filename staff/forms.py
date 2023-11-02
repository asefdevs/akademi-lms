from staff.models import Lessons, Students,Teachers
from baseuser.models import User
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import ClearableFileInput
from ckeditor.widgets import CKEditorWidget
from core.models import Classes,Settings
from staff.models import Sections
from django.db.models import Q



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

class EditStudentForm(forms.ModelForm):
    section = forms.ModelChoiceField(
        queryset=Sections.objects.all(),
        widget=forms.Select(attrs={'placeholder': 'Section','class': 'form-control form-control-sm'}),
        required=False
    )
    class Meta:
        model = Students
        fields = ('lesson',)
        widgets = {
            'lesson': forms.CheckboxSelectMultiple(attrs={'class':'form-check-input',}),
        }
           
    def __init__(self,*args,**kwargs):
        super(EditStudentForm,self).__init__(*args, **kwargs)
        active_season=str(Settings.objects.last())
        lessons=Lessons.objects.filter(season__season_name=active_season)
        self.fields['lesson'].queryset=lessons
        selected_lessons = self.instance.lesson.all()
        sections = Sections.objects.filter(section_of_lesson__in=selected_lessons)
        self.fields['section'].queryset = sections




class EditTeacherForm(forms.ModelForm):
    class Meta:
        model=Teachers
        fields=('about_teacher','position' )
        widgets={
            'about_teacher': CKEditorWidget(),
            'position': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Position'}),
        }

        


