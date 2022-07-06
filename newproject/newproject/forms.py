import imp
from turtle import textinput
from django import forms
from contact.models import contact
class contactform(forms.Form):
    Name=forms.CharField(required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    Email=forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Mobile=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),max_length=12)
    Message =forms.CharField(widget=forms.Textarea(attrs={'rows':3,'class':'form-control'}))
    Pic=forms.ImageField()

    class Meta:
        model = contact
        fields = ["Name","Email","Mobile","Message"]
