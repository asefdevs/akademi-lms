from staff.models import Student
from django import forms
class EditStudentForm(forms.ModelForm):
    class Meta:
        model=Student
        fields=('grade',)
        widgets={  
            'grade':forms.Select(attrs={'class':'form-control'}),
        }


