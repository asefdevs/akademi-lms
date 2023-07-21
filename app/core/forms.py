from typing import Any, Dict
from django import forms
from .models import ClassName
from staff.models import Student,Teacher,Lesson





class CreateClassForm(forms.ModelForm):
    class Meta:
        model=ClassName
        exclude = ['teachers']

        fields=('name','students','lessons','teachers',)
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'students': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students'}),
            'lessons': forms.CheckboxSelectMultiple(attrs={'placeholder':'Lessons', 'class': 'lesson-select'}),
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
    

class DefineTeachersForm(forms.ModelForm):
    class Meta:
        model=ClassName
        fields=('name','teachers','lessons','students')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control','readonly':'readonly'}),
            'students': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students','readonly':'readonly'}),
            'lessons': forms.CheckboxSelectMultiple(attrs={'placeholder':'Lessons','readonly':'readonly'}),
            'teachers': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].widget=forms.MultipleHiddenInput()
        self.fields['lessons'].widget=forms.MultipleHiddenInput()

        
        if 'lessons' in self.initial:
            selected_lessons = self.initial.get('lessons')
            self.fields['teachers'].queryset = Teacher.objects.filter(position__title__in=selected_lessons)
        else:
            self.fields['teachers'].queryset = Teacher.objects.none()

class EditClassForm(forms.ModelForm):

    class Meta:
        model=ClassName
        fields=('name','students','lessons','teachers')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'students': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students',}),
            'lessons': forms.CheckboxSelectMultiple(attrs={'placeholder':'Lessons',}),
            'teachers': forms.CheckboxSelectMultiple()
        }

    def __init__(self,*args, **kwargs):
        super(EditClassForm,self).__init__(*args,**kwargs)
        class_name=self.instance.name
        class_instance = ClassName.objects.get(name=class_name)
        students_of_class = class_instance.students.all()
        print(students_of_class)
        # for student in students_of_class:




        #     exist_student=ClassName.objects.filter(students__grade=class_name)
        #     if exist_student.exists():
        #         students=students.get(user__username=student)
        # self.fields['students'].queryset=students
        # if not students.exists():
        #     students = Student.objects.none()
        #     self.fields['students'].queryset = students
        #     self.fields['students'].empty_label = 'No unregistered student found'
        #     self.errors['students']='x'
            
            


    


