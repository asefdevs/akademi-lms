from typing import Any, Dict
from django import forms
from . models import Classes,Seasons
from staff.models import Students,Sections,Lessons






class CreateClassForm(forms.ModelForm):
    class Meta:
        model=Classes
        fields=('name','student')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'student': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students'}),        
        }
    def __init__(self, *args, **kwargs):
        super(CreateClassForm,self).__init__(*args, **kwargs)
        students=Students.objects.all()
        for student in students:
            exist_student=Classes.objects.filter(student__user__username=student)
            if exist_student.exists():
                students=students.exclude(user__username=student)
        self.fields['student'].queryset=students
        if not students.exists():
            students = Students.objects.none()
            self.fields['student'].queryset = students
            self.fields['student'].empty_label = 'No unregistered student found'
            self.errors['student']='x'


    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    
    def clean_name(self):
        name=self.cleaned_data.get('name')
        if name:
            if Classes.objects.filter(name=name).exists():
                self.add_error('name', 'This class already exists')
        return name
    

from itertools import chain

class EditClassForm(forms.ModelForm):
    class Meta:
        model=Classes
        fields=('name','student',)
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Class Name','class':'form-control'}),
            'student': forms.CheckboxSelectMultiple(attrs={'placeholder':'Students',}),

        }

    def __init__(self,*args,**kwargs):
        super(EditClassForm, self).__init__(*args,**kwargs)
        all_students = Students.objects.all()
        student_of_classes = []
        student_of_other_classes=[]

        for student in all_students:
            if student in self.instance.student.all():
                status = student.class_of_students.last() 
                student_of_classes.append((student.pk, f"{student} - {status}"))
            else:
                status = student.class_of_students.last()
                student_of_other_classes.append((student.pk, f"{student} - {status}"))
        student_choices = list(chain(student_of_classes, student_of_other_classes))


        self.fields['student'].choices = student_choices
        print(self.fields['student'].choices)



class AddLessonForm(forms.ModelForm):
    class Meta:
        model=Lessons
        fields=('title', 'season','section',)
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'season':forms.Select(attrs={'class':'form-control'}),
            'section':forms.SelectMultiple(attrs={'class':'form-select'}),
        }
    def __init__(self,*args,**kwargs):
        super(AddLessonForm, self).__init__(*args,**kwargs)
        self.fields['section'].widget=forms.MultipleHiddenInput()
    def clean(self) :
        cleaned_data= super().clean()
        return cleaned_data
    def clean_title(self):
        title= self.cleaned_data.get('title')
        if Lessons.objects.filter(title=title).exists():
            self.add_error('title','Lesson title already exists')
        return title

class AddSectionForm(forms.ModelForm):
    class Meta:
        model=Sections
        fields=('title','teacher','students','max_student_count',)
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'teacher': forms.Select(attrs={'class':'form-select '}),
            'students': forms.CheckboxSelectMultiple(attrs={'class':'form-check-input','type':'checkbox',}),
            'max_student_count': forms.NumberInput(attrs={'class':'form-control'}),
        }
    # def __init__(self,*args,**kwargs):
    #     super(AddSectionForm, self).__init__(*args,**kwargs)
    #     all_students=Students.objects.all()
    #     for student in self.fields['students']:
    #         print('+++++++')



class EditLessonForm(forms.ModelForm):
    class Meta:
        model=Lessons
        fields=('title', 'season','section',)
        widget={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'season':forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
        }

class EditSectionForm(forms.ModelForm):
    class Meta:
        model=Sections
        fields=('title','teacher','students','max_student_count',)
        widgets={
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'teacher': forms.Select(attrs={'class':'form-select '}),
            'students': forms.CheckboxSelectMultiple(attrs={'class':'form-check-input','type':'checkbox', 'id':'studid'}),
            'max_student_count': forms.NumberInput(attrs={'class':'form-control'}),
        }
