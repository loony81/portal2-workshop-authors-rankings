from django import forms

class AuthorNameForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={
        'placeholder':'Search...',
        'class': 'form-control',
        'aria - label': 'Input group example',
        'aria - describedby': 'button-addon'
    }), max_length=50)