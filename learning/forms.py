
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from .models import Inscrit


User = get_user_model()
#créer la classe heritant de ModelForm


class InscritForm(forms.ModelForm):

  class Meta:
    model = Inscrit

    fields = ['username', 'first_name', 'last_name', 'email', 'password', 'photo']

    widgets = {
      'username':forms.TextInput(attrs={'class':'form-control'}),
      'first_name': forms.TextInput(attrs={'class':'form-control'}),
      'last_name': forms.TextInput(attrs={'class':'form-control'}),
      'email': forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
      'password':forms.PasswordInput(attrs={'class':'form-control'}),

    }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Nom d'utilisateur",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(max_length=100, label="Mot de passe",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))






class ContactForm(forms.Form):

  subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Sujet'}))

  message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'cols':20, 'rows':8, 'placeholder':'Message'}))

  sender = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Votre adresse e-mail'}))

  cc_myself = forms.BooleanField(required=False)




class SettingsForm(forms.ModelForm):

    class Meta:
        model = Inscrit

        fields = ['first_name', 'last_name', 'email', 'photo']

        widgets = {

            'first_name': forms.TextInput(attrs={'class': 'form-control'}),

            'last_name': forms.TextInput(attrs={'class': 'form-control'}),

            'email': forms.TextInput(attrs={'class': 'form-control'}),

        }




class MyPasswordChangeForm(PasswordChangeForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for fieldname in ['old_password', 'new_passord1', 'new_password2']:
      self.fields[fieldname].widget.attrs={'class':'form-control'}


