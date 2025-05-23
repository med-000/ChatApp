from django import forms
from .models import MyProfile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = MyProfile
        fields = ['user_id', 'nickname', 'email', 'profile', 'birthday', 'avater']
        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control', 'size': 40}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'size': 30}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': 40}),
            'profile': forms.TextInput(attrs={'class': 'form-control', 'size': 20}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avater': forms.ClearableFileInput(attrs={'class': 'form-control-file'})
        }
