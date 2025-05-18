from django import forms
from accounts.models import User, Student, Teacher, Parent, Subject



class AddSubjectForm(forms.Form):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), label="Select Subject")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'teacher'):
            self.fields['subject'].queryset = Subject.objects.exclude(id__in=user.teacher.subjects.values_list('id', flat=True))


class CreateSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']


class AddChildForm(forms.Form):
    child = forms.ModelChoiceField(queryset=Student.objects.none(), label="Select Child")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'parent'):
            self.fields['child'].queryset = Student.objects.exclude(user_id__in=user.parent.children.values_list('user_id', flat=True))

