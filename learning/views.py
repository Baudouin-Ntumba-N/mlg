
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login, logout
#from django.contrib import messages
from .forms import ContactForm, InscritForm, ModifyForm, ModiForm
from .models import Document, HomeCoverImage, Contact
from articles.models import Article
from shopping.models import Cart
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
#from django.contrib.sites.shortcuts import get_current_site

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from django.core.paginator import Paginator
import os
#import smtplib
from django.conf import settings


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InscritSerializer, EndSignupSerializer
from .serializers import UserSerializer
from rest_framework import permissions, generics
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from knox.views import LoginView as knoxLoginView


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
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == 'POST':
        form = InscritForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']


            recipients = [f"{email}"]
            try:
                user = User.objects.create_user(username = username, first_name = first_name, last_name = last_name, email = email, password = password, is_active=False)
                user.save()
                #current_site = get_current_site(request)
                subject = 'Activez votre compte.'
                message = render_to_string('learning/acc_active_email.html', {
                'user': user,
                'domain': "mlglearning.com",
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

                send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=True)

                return render(request, 'learning/email_confirm.html', {"first_name":user.first_name})

                #return render(request, 'learning/welcome.html', {"login_welcome_msg":f"{user.first_name}, Bienvenue sur MLG"})
            except:
                return render(request, 'learning/signup.html', {"signupError":"Echec! Un autre compte possède peut-être déjà ce nom d'utilisateur!"})
        return redirect('signup')
    return render(request, 'learning/signup.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("<div style='background-color:lightgray;height:400px;color:darkgreen;font-size:30px;'> <br> <h1> Merci d'avoir confirmé votre email. Vous pouvez maintenant vous <a href='https://www.mlglearning.com/login/'>connecter</a>.</h1> </div>")
    else:
        return HttpResponse("Lien d'activation invalide!")



def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

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
    msg = f.cleaned_data['message']
    sender = f.cleaned_data['sender']
    cc_myself = f.cleaned_data['cc_myself']

    message = f"Nouveau contact de {sender} \n \n {msg}"

    recipients = ["bdnntumba@gmail.com"]


    if cc_myself:
      recipients.append(sender)


    send_mail(subject, message, settings.EMAIL_HOST_USER, recipients, fail_silently=False)
    contact = Contact(subject=subject, message=msg, email=sender)
    contact.save()

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
    if request.FILES:
      f = ModifyForm(request.POST, request.FILES)
    #if photo not updated
    else:
      f = ModiForm(request.POST)

    #check whether f is valid
    if f.is_valid():

      try:
          inscrit = User.objects.get(username=request.POST['username'])
      except:
          return redirect("settings")

      if len(request.FILES) == 0:
        #update process
        inscrit.username = f.cleaned_data['username']
        inscrit.first_name = f.cleaned_data['first_name']
        inscrit.last_name = f.cleaned_data['last_name']
        inscrit.email = f.cleaned_data['email']
        inscrit.save()

      else:
        #photo updated
        #update process
          inscrit.username = f.cleaned_data['username']
          inscrit.first_name = f.cleaned_data['first_name']
          inscrit.last_name = f.cleaned_data['last_name']
          inscrit.email = f.cleaned_data['email']

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








#OUR API SERVICE

class SignupAPI(generics.GenericAPIView):
    serializer_class = InscritSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]

        })


@api_view(['PUT'])
def end_signup_api(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        user.DoesNotExist()

    if request.method == 'PUT':

        serializer = EndSignupSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    return Response(status=status.HTTP_204_NO_CONTENT)


class LoginAPI(knoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response({
            "user": UserSerializer(user).data["id"],
            "token":  AuthToken.objects.create(user)[1]})

