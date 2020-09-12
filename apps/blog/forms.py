from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *

class MailForm(forms.Form):
    name = forms.CharField(required = True, widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required = True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    body = forms.CharField(required = True, widget=forms.Textarea(attrs={'class':'form-control'}))

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id':'name'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'id':'body'})
        }
