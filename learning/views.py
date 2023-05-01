from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib import messages
from .forms import*
from .models import Document, HomeCoverImage
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
    documents = documents.order_by('-id')[:2]

    context = {'home_cover_image':home_cover_image, 'articles':articles, 'documents':documents}
    return render(request, 'learning/index.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = InscritForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password)
                login(request, user)
                return render(request, 'learning/welcome.html', {"login_welcome_msg":f"{user.first_name}, Bienvenue sur MLG"})
            except:
                return render(request, 'learning/signup.html', {"signupError":"Echec! Un autre compte possède déjà ce nom d'utilisateur!"})
        return redirect('signup')
    return render(request, 'learning/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user:
            login(request, user)
            return redirect("welcome")
        else:
            context = {"login_failure_msg":"Nom d'utilisateur ou mot de passe incorrects!"}
            return render(request, 'learning/login.html', context)
    return render(request, 'learning/login.html')


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
    #receiver = 'bdnntumba@gmail.com'

    recipients = [sender]
    fail_silently = False

    if cc_myself:
      recipients.append(settings.EMAIL_HOST_USER)



    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #server.login("bdnntumba@gmail.com", settings.EMAIL_HOST_PASSWORD)
    #server.sendmail(subject, settings.EMAIL_HOST_USER, sender,  message, fail_silently)
    #server.quit()



    #

    #subject = f.cleaned_data['subject']
    #message = f.cleaned_data['message']
    #sender = f.cleaned_data['sender']
    #cc_myself = f.cleaned_data['cc_myself']
    #receiver = 'bdnntumba@gmail.com'

    #recipients = [receiver]
    #fail_silently = False

    #if cc_myself:
      #recipients.append(sender)



    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #server.login("bdnntumba@gmail.com", settings.EMAIL_HOST_PASSWORD)
    #server.sendmail(subject, settings.EMAIL_HOST_USER, sender,  message, fail_silently)
    #server.quit()

    send_mail(subject, message, settings.EMAIL_HOST_USER , recipients, fail_silently)

    form = ContactForm()
    return render(request, 'learning/contact.html', {'msg_sent':'Message envoyé!', 'form':form})

  form = ContactForm()
  return render(request, 'learning/contact.html', {'form':form})


def welcome_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    articles = Article.objects.all()
    articles = articles.order_by('-id')
    myarticles = articles[0:4]
    return render(request, 'learning/welcome.html', {"articles": myarticles})


def about_view(request):
  return render(request, 'learning/about.html')


def settings_view(request):

  #if data sent by POST method
  if request.method=="POST":

    #Initialize. form used if profile photo is sent too
    #f = ModifyForm(request.POST, request.FILES)

    #if photo updated
    if len(request.FILES) != 0:
      f = ModifyForm(request.POST, request.FILES)
    #if photo not updated
    else:
      f = ModiForm(request.POST)

    #check whether f is valid
    if f.is_valid():
      inscrit = User.objects.get(username=request.POST['username'])
      if len(request.FILES) == 0:
        #update process
        inscrit.username = f.cleaned_data['username']
        inscrit.first_name = f.cleaned_data['first_name']
        inscrit.last_name = f.cleaned_data['last_name']
        inscrit.email = f.cleaned_data['email']
       # inscrit.password = f.cleaned_data['password']
        inscrit.save()
      else:
        #photo updated
        #update process
          inscrit.username = f.cleaned_data['username']
          inscrit.first_name = f.cleaned_data['first_name']
          inscrit.last_name = f.cleaned_data['last_name']
          inscrit.email = f.cleaned_data['email']
          #inscrit.password = f.cleaned_data['password']

          if inscrit.photo == "photos/default.jpg":
            inscrit.photo = f.cleaned_data['photo']
          else:
            os.remove(inscrit.photo.path)
            inscrit.photo = f.cleaned_data['photo']

          inscrit.save()


      return render(request, 'learning/welcome.html', {'modif': 'Modifications enregistrées'})

    #if f is not valid
    else:
      return render(request, 'learning/settings.html', {'msm':'Echec de modifications!'})

  form = InscritForm()
  return render(request, 'learning/settings.html', {'form':form})



# def password_change_done_view(request):
#   return render(request, 'learning/password_change_done.html')



#liste des documents
def documents_list_view(request):
  documents = Document.objects.all()
  page = Paginator(documents, 10)
  page_number = request.GET.get('page')
  this_page = page.get_page(page_number)
  return render(request, 'learning/documents_list.html', {'page':this_page})


def doc_details_view(request, slug):
  try:
    cart = Cart.objects.get(shopper=request.user)
  except:
    cart =""

  document = Document.objects.get(slug = slug)
  return render(request, 'learning/doc_details.html', {'cart':cart, 'document':document})