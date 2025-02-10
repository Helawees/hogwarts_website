from django import forms


class StudentsForm(forms.Form):
    first_name = forms.CharField(
        max_length=29,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'name': 'first_name',
            'placeholder': "Enter new student's First Name"
        })
    )
    last_name = forms.CharField(
        max_length=30,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'name': 'last_name',
            'placeholder': "Enter new student's Last Name"
        })
    )