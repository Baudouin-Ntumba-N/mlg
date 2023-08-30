from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from django.views import View
from .forms import*
from .models import Document, AboutUs, HomeCoverImage
from articles.models import Article
from shopping.models import Cart
from django.core.mail import send_mail
from django.core.paginator import Paginator
import os

import smtplib
from django.conf import settings

User = get_user_model()



def index_view(request):
    try:
      home_cover_image = HomeCoverImage.objects.get(pk=1)
    except:
      home_cover_image = ""

    myarticles = Article.objects.filter(published = True)
    articles = myarticles.order_by('-pub_date')[: 2]
    documents = Document.objects.all()
    context = {'home_cover_image':home_cover_image, 'articles':articles, 'documents':documents}
    return render(request, 'learning/index.html', context)


def signup_view(request):
  form = InscritForm()
  if request.method == "POST":
    f = InscritForm(request.POST)
    if f.is_valid():
      username = f.cleaned_data['username']
      first_name = f.cleaned_data['first_name']
      last_name = f.cleaned_data['last_name']
      email = f.cleaned_data['email']
      password = f.cleaned_data['password']


      user = User.objects.create_user(
          username = username,
          first_name = first_name,
          last_name = last_name,
          email = email,
          password = password
      )

      login_form = LoginForm()
      return render(request, 'learning/login.html', {'msg':f'{first_name}, votre compte a été créé avec succès !', 'form':login_form})

    return render(request, 'learning/signup.html')

  return render(request, 'learning/signup.html', {'form':form})





def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username = username, password = password)

            if user:
                login(request, user)
                context = {'login_msg':'Vous êtes connecté(e)...'}
                return render(request, 'learning/welcome.html', context)
            else:
                context = {"error_msg":"Nom d'utilisateur ou mot de passe incorrects!",
                          'form': LoginForm()}
                return render(request, 'learning/login.html', context)
        return redirect("login")
    return render(request, 'learning/login.html', {'form': LoginForm()})


def logout_view(request):
    logout(request)
    return redirect('login')


def contact_view(request):
  f = ContactForm(request.POST)
  if f.is_valid():
    subject = f.cleaned_data['subject']
    message = f.cleaned_data['message']
    sender = f.cleaned_data['sender']
    cc_myself = f.cleaned_data['cc_myself']

    recipients = [sender]


    if cc_myself:
      recipients.append(sender)

    send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=True)
    return render(request, 'learning/contact.html', {'msg_sent':'Message envoyé!', 'form':ContactForm()})

  form = ContactForm()
  return render(request, 'learning/contact.html', {'form':form})


def welcome_view(request):
	return render(request, 'learning/welcome.html', )


def about_view(request):
    all_about_us = AboutUs.objects.all()
    about_us = all_about_us[0]
    return render(request, 'learning/about_us.html', {'about_us':about_us})




class Settings(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
        	return redirect("login")
        form = SettingsForm(instance=request.user)
        return render(request, "learning/settings.html", {"form":form})

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
        	return redirect("login")
        user = User.objects.get(pk = request.user.id)
        form = SettingsForm(instance=user, data=request.POST, files=request.FILES)
        if form.is_valid():
            if str(user.photo) == "photos/default.jpg":
                form.save()
            else:
                if len(request.FILES) != 0:
                    print("hello", request.FILES['photo'])
                    os.remove(request.user.photo.path)
                    form.save()
                else:
                    form.save()
            messages.success(request, "Modifications enregistrées avec succès!")
            return redirect("settings")
        return redirect("settings")




#liste des documents
def documents_list_view(request):
  documents = Document.objects.all()
  page = Paginator(documents, 2)
  page_number = request.GET.get('page')
  this_page_documents = page.get_page(page_number)
  return render(request, 'learning/documents_list.html', {'page':this_page_documents})


def doc_details_view(request, slug):
  try:
    cart = Cart.objects.get(shopper=request.user)
  except:
    cart =""

  document = Document.objects.get(slug = slug)
  return render(request, 'learning/doc_details.html', {'cart':cart, 'document':document})