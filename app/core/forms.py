from django import forms
from .models import ClassName
from staff.models import Student





class CreateClassForm(forms.ModelForm):
    class Meta:
        model=ClassName
        fields=('name','students','lessons')
        widgets={
            'name': forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}),
            'students': forms.SelectMultiple(attrs={'placeholder':'FirstName','class':'form-control'}),
            'lessons': forms.SelectMultiple(attrs={'placeholder':'LastName','class':'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def clean_students(self):
        students = self.cleaned_data.get('students')
        if students:
            for student in students:
                if ClassName.objects.filter(students__user__username=student).exists():
                     self.add_error('students', f"The student '{student}' already exists in another class.")

        return students









#   cag kimidi 
# class EditStudentForm(forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.filter(user_type='student'))
#     password=None
#     class Meta:
#         model=Student
#         fields=('grade',)
#         widgets={  
#             'user':forms.Select(attrs={'class':'form-control','placeholder':'user select','name':"student_id" ,'id':"student_id"}),
#             'grade':forms.Select(attrs={'class':'form-control'}),
#         }
