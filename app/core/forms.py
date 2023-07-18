from typing import Any, Dict
from django import forms
from .models import ClassName
from staff.models import Student,Teacher,Lesson





class CreateClassForm(forms.ModelForm):
    class Meta:
        model=ClassName
        exclude = ['teachers']

        fields=('name','students','lessons','maximum_student')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'students': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students'}),
            'lessons': forms.CheckboxSelectMultiple(attrs={'placeholder':'Lessons',}),
            'maximum_student':forms.NumberInput(attrs={'placeholder':'max_student',}),
            'teachers': forms.CheckboxSelectMultiple()
        }



    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_name(self):
        name=self.cleaned_data.get('name')
        if name:
            if ClassName.objects.filter(name=name).exists():
                self.add_error('name', 'This class already exists')
        return name

    def clean_students(self):
        students = self.cleaned_data.get('students')
        if students:
            for student in students:
                if ClassName.objects.filter(students__user__username=student).exists():
                     self.add_error('students', f"The student '{student}' already exists in another class.")

        return students


class EditClassForm(forms.ModelForm):

    class Meta:
        model=ClassName
        fields=('name','students','lessons','maximum_student','teachers')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'students': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students',}),
            'lessons': forms.CheckboxSelectMultiple(attrs={'placeholder':'Lessons',}),
            'maximum_student':forms.NumberInput(attrs={'placeholder':'max_student',}),
            'teachers': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'lessons' in self.initial:
            selected_lessons = self.initial.get('lessons')
            self.fields['teachers'].queryset = Teacher.objects.filter(position__title__in=selected_lessons)
        else:
            self.fields['teachers'].queryset = Teacher.objects.none()
    





    # def clean(self) :
    #     cleaned_data=super().clean()
    #     return cleaned_data
    
    # def clean_lessons(self):
    #     lesson_data=self.cleaned_data.get('lessons')


    
    


