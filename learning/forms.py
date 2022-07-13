
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

      'password':forms.PasswordInput(),

    }







class ContactForm(forms.Form):

  subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Sujet'}))

  message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message'}))

  sender = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Votre adresse e-mail'}))

  cc_myself = forms.BooleanField(required=False)


class ModifyForm(forms.Form):

  username = forms.CharField(max_length=100)

  first_name = forms.CharField(max_length=100)

  last_name = forms.CharField(max_length=100)

  email = forms.EmailField()

  #password = forms.CharField(max_length=100)

  photo = forms.FileField()




class ModiForm(forms.Form):

  username = forms.CharField(max_length=100)

  first_name = forms.CharField()

  last_name = forms.CharField()

  email = forms.EmailField()

  #password = forms.CharField(max_length=100)



class ContactForm(forms.Form):

  subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder':'Sujet'}))

  message = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Message'}))

  sender = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Adresse e-mail'}))

  cc_myself = forms.BooleanField(required=False)


class MyPasswordChangeForm(PasswordChangeForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for fieldname in ['old_password', 'new_passord1', 'new_password2']:
      self.fields[fieldname].widget.attrs={'class':'form-control'}



#class ModifyForm(forms.ModelForm):

 # class Meta:
#    model = Inscrits

 #   fields = ('nom', 'prenom', 'email', 'passwd', 'photo')


# Modif form if file photo not updated

#class ModiForm(forms.ModelForm):

 # class Meta:
   # model = Inscrits

    #fields = ('nom', 'prenom', 'email', 'passwd')



#class UpdateProfileForm(forms.Form):
  #photo = forms.CharField(widget=forms.FileInput())