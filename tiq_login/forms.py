from django import forms
from django.contrib.auth.forms import AuthenticationForm

class PasswordChangeForm(forms.Form):
   username = forms.CharField(max_length=16)
   old_password = forms.CharField(max_length=16, widget=forms.PasswordInput)
   new_password_1 = forms.CharField(max_length=16, widget=forms.PasswordInput)
   new_password_2 = forms.CharField(max_length=16, widget=forms.PasswordInput)
   
   def clean(self):
      if (self.cleaned_data['new_password_1'] != self.cleaned_data['new_password_2']):
         raise forms.ValidationError("New Passwords must Match")
      return self.cleaned_data

class SignupForm(forms.Form):
   fullname = forms.CharField(max_length=32)
   username = forms.CharField(max_length=16)
   password = forms.CharField(max_length=16, widget=forms.PasswordInput)
   email = forms.EmailField()
   orgcode = forms.CharField(max_length=6, required=False)
   

class RememberAuthenticationForm (AuthenticationForm):
   remember = forms.BooleanField(required=False)