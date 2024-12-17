from django import forms 
from .models import Customer

class LoginForm(forms.ModelForm):
    number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Customer
        fields = ['number']

    