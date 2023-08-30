from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from articles.models import Article, Comment
from .forms import CommentForm, ReplyForm, ArticleForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, authenticate, login, logout

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




User = get_user_model()


def articles_list_view(request):
    articles = Article.objects.all()
    articles = articles.order_by('-pub_date')
    top_article = articles.first()

    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)

    return render(request, 'articles/list.html', {'page':thispage})


def article_details_view(request, slug):
    try:
    	article = Article.objects.get(slug=slug)
    except:
    	return redirect('/articles/')

    comments_number = Comment.objects.filter(commented_article=article).count()

    parents = (Comment.objects.filter(commented_article=article, parent=None)).order_by('-post_date')

    return render(request, 'articles/details.html', {'article':article, 'comments':parents, 'comments_number':comments_number})


def create_article_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    form = ArticleForm()
    if request.method == "POST":
        if request.user.is_authenticated:
	        f = ArticleForm(request.POST, request.FILES)
	        if f.is_valid():
	            f.save()
	            return redirect("articles")
        	else:
        	    return redirect("create-article")

        return redirect("login")

    return render(request, 'articles/create_article.html', {'form':form})


def update_article_view(request, slug):
    if not request.user.is_authenticated:
        return redirect("login")

    try:
        article = Article.objects.get(slug=slug)
    except KeyError:
        return redirect("articles")
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(instance=article, data = request.POST, files=request.FILES)
        if form.is_valid():
        	form.save()
        	return redirect(reverse("article-details", kwargs={"slug": slug}))
        else:
            return redirect(reverse("update-article", kwargs={"slug": slug}))
    return render(request, 'articles/update_article.html', {'form':form})


#pour laissser un commentaire
def comment_view(request):

  if request.method == "POST":
    if not request.user.is_authenticated:
      return redirect('login')
    #if sender auhenticated
    f = CommentForm(request.POST)
    if f.is_valid():
      #get the logged in user and his comment
      inscrit = User.objects.get(pk=request.user.id)
      comment = f.cleaned_data['comment']

      #check whether comment is related to an article or to MLG
      if  request.POST['article_slug']!="blabla":
        article = Article.objects.get(slug=request.POST['article_slug'])

        #save the comment in the table and get all comments related to the article
        c = Comment(writer=inscrit, comment_content=comment, commented_article=article)
        c.save()
        comments = (Comment.objects.filter(commented_article=article)).order_by('-post_date')
        return redirect(f"/articles/{article.slug}")

      else:
        c = Comment(writer=inscrit, comment_content=comment)
        c.save()
        return render(request, 'learning/welcome.html', {'comment_report':'Commentaire envoyé avec succès!'})

    else:
      return render(request, 'learning/welcome.html', {'comment_failure':"Echec d'envoi!"})

  else:
    return redirect('home')



#to access the form designed to send a reply
def reply_view(request, token):
  if request.user.is_authenticated:
    comment = Comment.objects.get(token=token)
    return render(request, 'articles/reply.html', {'comment':comment})
  else:
    return redirect('login')

#insertion d'une reponse
def replying_view(request):

  comment = get_object_or_404(Comment, token=request.POST.get('token'))
  try:
    replies = Comment.objects.filter(parent=comment)
  except:
    replies = ""
  if request.method == "POST":
    f = ReplyForm(request.POST)
    if f.is_valid():
      replier = get_object_or_404(User, pk=request.user.id)
      reply_content = f.cleaned_data['reply_content']
      reply = Comment(writer=replier, comment_content=reply_content, commented_article=comment.commented_article, parent=comment)

      reply.save()

      return redirect(reverse("comment-replies", kwargs={ "token": comment.token}))

    else:
      return render(request, 'articles/replies.html', {'comment':comment, 'replies':replies, 'authen':'Réponse invalide!'})
  else:
    return redirect('/articles/')


#pour voir les reponses à un commentaire
def comment_replies_view(request, token):

  try:
    comment = Comment.objects.get(token=token)
  except:
    return redirect('/articles/')
    #get all replies related to the comment
  replies = Comment.objects.filter(parent=comment).order_by('-post_date')

  return render(request, 'articles/replies.html', {'replies':replies, 'comment':comment})




def delete_comment_view(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    article = Article.objects.get(pk=comment.commented_article.id)
    comment.delete()
    context = {'article':article, 'comments':Comment.objects.filter(commented_article=article, parent=None)}

    return redirect(reverse("article-details", kwargs={"slug":article.slug}))


def delete_reply_view(request, reply_id):
    try:
      reply = Comment.objects.get(pk=reply_id)
    except:
      return redirect("articles")
    parent_id = reply.parent.id
    reply.delete()
    return redirect(f"/articles/comment/replies/{parent_id}")




def like_article(request, article_slug):
    try:
        article = Article.objects.get(slug=article_slug)
    except KeyError:
        return redirect("home")

    if not request.user.is_authenticated:
        return redirect("login")

    if not request.user in article.likes.all():
        article.likes.add(request.user)
        return redirect(reverse("article-details", kwargs={"slug":article_slug}))
    else:
        article.likes.remove(request.user)
        return redirect(reverse("article-details", kwargs={"slug":article_slug}))







#api
@api_view(["GET", "POST"])
def article_list(request):

  if request.method == 'GET':
    articles = Article.objects.all()
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)

  elif request.method == 'POST':
    serializer = ArticleSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def article_detail(request, pk):
  try:
    article = Article.objects.get(pk=pk)
  except:
    article.DoesNotExist()

  if request.method == "GET":
    article_serializer = ArticleSerializer(article)

    #comments = Comment.objects.filter(commented_article = article, parent=None)
    #comments_serializer = CommentSerializer(comments)

    return Response(article_serializer.data)

  elif request.method == "PUT":
    serializer = ArticleSerializer(article, data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  elif request.method == "DELETE":
    article.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(["GET", "POST"])
def reply_api(request, parent_id):
  parent = Comment.objects.get(pk = parent_id)

  if request.method == "POST":
    serializer = CommentSendSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response()
    else:
      return Response({"error":"BAD REQUEST!"})

  elif request.method == "GET":
    replies = Comment.objects.filter(parent = comment)
    serializer = CommentSerializer(replies, many=True)

    return Reponse(serializer.data)