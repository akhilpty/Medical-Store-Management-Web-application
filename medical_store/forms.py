from django import forms

from .models import Medicine


class SignupForm(forms.Form):
     username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', 'placeholder': 'Username'}), required=True)
     firstname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Firstname'}), required=True)
     lastname = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Lastname'}), required=True)
     emailid = forms.CharField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'EmailId'}), required=True)
     password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True)

class LoginForm(forms.Form):
     username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control ', 'placeholder': 'Username'}), required=True)
     password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True)


class MedicalEditform(forms.ModelForm):
    class Meta:
        model=Medicine
        fields= '__all__'
class Medicalupdateform(forms.ModelForm):
    class Meta:
        model=Medicine
        fields= ['medicine_name','medicine_type','price','count','medicine_company']