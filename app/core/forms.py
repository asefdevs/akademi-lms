from datetime import timezone
from django import forms
from . models import Classes,Assignment, StudentsAssignment
from staff.models import Students,Sections,Lessons
from ckeditor.widgets import CKEditorWidget






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

    def clean(self) :
        cleaned_data= super().clean()
        return cleaned_data
    def clean_max_student_count(self):
        max= self.cleaned_data.get('max_student_count')
        students=self.cleaned_data.get('students')
        count_of_students=students.count()
        if int(count_of_students) > int(max):
            self.add_error('max_student_count','Exceeded max student count')
        return max


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

class CreateAssignmentForm(forms.ModelForm):
    receiver = forms.ModelMultipleChoiceField(
        queryset=Sections.objects.all(),
        widget=forms.SelectMultiple(attrs={'placeholder': 'Section','class': 'form-control',}),
        required=False
    )
    class Meta:
        model = Assignment
        fields = ('title','max_try','deadline','description','lesson','receiver','sender',) 
        widgets={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'max_try':forms.NumberInput(attrs={'class':'form-control'}),
            'deadline':forms.DateTimeInput(attrs={'class':'form-control',}),
            'description':CKEditorWidget(),
            'lesson':forms.Select(attrs={'placeholder':'User Type','class':'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(CreateAssignmentForm, self).__init__(*args, **kwargs)

        lesson_initial = self.initial.get('lesson')
        if lesson_initial:
            self.fields['receiver'].queryset = Sections.objects.filter(section_of_lesson=lesson_initial)
        else:
            self.fields['receiver'].queryset = Sections.objects.all()

        self.fields['sender'].widget = forms.HiddenInput()
        self.fields['lesson'].widget = forms.HiddenInput()


class StudentAssigmentForm(forms.ModelForm):

    class Meta:
        model = StudentsAssignment
        fields = '__all__' 
       

    def __init__(self, *args, **kwargs):
        super(StudentAssigmentForm, self).__init__(*args, **kwargs)
        self.fields['assignment'].widget = forms.HiddenInput()




    