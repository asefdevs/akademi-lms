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
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateClassForm,self).__init__(*args, **kwargs)
        students=Student.objects.all()
        for student in students:
            exist_student=ClassName.objects.filter(students__user__username=student)
            if exist_student.exists():
                students=students.exclude(user__username=student)
        self.fields['students'].queryset=students
        if not students.exists():
            students = Student.objects.none()
            self.fields['students'].queryset = students
            self.fields['students'].empty_label = 'No unregistered student found'
            self.errors['students']='x'
            

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_name(self):
        name=self.cleaned_data.get('name')
        if name:
            if ClassName.objects.filter(name=name).exists():
                self.add_error('name', 'This class already exists')
        return name
    
    def clean_maximum_students(self):
        max_students=self.cleaned_data.get('maximum_student')
        students = self.cleaned_data.get('students')
        print(students.count())
        if  students.count() > max_students:
            print(students.count())
            self.add_error('maximum_student','Count of Students exceeded maximum limit')
        return max_students


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


    
    


