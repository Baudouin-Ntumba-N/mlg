from django.shortcuts import render, redirect, get_object_or_404
from articles.models import Article, Comment
from .forms import CommentForm, ReplyForm, ArticleForm, UpdateArticleForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model


User = get_user_model()

def articles_list_view(request):
    articles = Article.objects.all()
    articles = articles.order_by('-pub_date')

    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)

    return render(request, 'articles/list.html', {'page':thispage})


def article_details_view(request, slug):

    try:
      article = Article.objects.get(slug=slug)
    except:
      return redirect('/articles/')

    comments = (Comment.objects.filter(commented_article=article, parent=None)).order_by('-post_date')
    comments_number = Comment.objects.filter(commented_article=article).count()
    return render(request, 'articles/details.html', {'article':article, 'comments':comments, 'comments_number':comments_number})

def edit_article_view(request):
  form = ArticleForm()

  if request.method == "POST":
    if request.user.is_authenticated:
        f = ArticleForm(request.POST, request.FILES)
        if f.is_valid():
          if f.cleaned_data['author'] != request.user:
              return redirect("edit-article")
          f.save()
          return redirect("articles")
        else:
          return redirect("edit-article")
    else:
        return redirect("login")

  return render(request, 'articles/edit_article.html', {'form':form})


def update_article_view(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except:
        return redirect("articles")

    form = UpdateArticleForm(instance=article)
    if request.method=='POST':
        if not request.user.is_authenticated:
            return redirect('login')
        f = UpdateArticleForm(request.POST, request.FILES, instance=article)
        if f.is_valid():
            f.save()
            return redirect('articles')
        else:
            return redirect(f'/articles/update-article/{slug}')

    return render(request, 'articles/update_article.html', {'form': form})



def articles_english_view(request):
    articles = Article.objects.filter(categorie=1)
    articles = articles.order_by('-pub_date')
    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)

    return render(request, 'articles/articles_english.html', {'page':thispage})



def articles_maths_view(request):
    articles = Article.objects.filter(categorie=2)
    articles = articles.order_by('-pub_date')
    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)
    return render(request, 'articles/articles_maths.html', {'page':thispage})

def articles_geoscience_view(request):
    articles = Article.objects.filter(categorie=3)
    articles = articles.order_by('-pub_date')
    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)
    return render(request, 'articles/articles_geoscience.html', {'page':thispage})


def articles_cs_view(request):
    articles = Article.objects.filter(categorie=4)
    articles = articles.order_by('-pub_date')
    page = Paginator(articles, 4)
    pagenumber = request.GET.get('page')
    thispage = page.get_page(pagenumber)
    return render(request, 'articles/articles_cs.html', {'page':thispage})





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
      content = f.cleaned_data['content']

      #check whether comment is related to an article or to MLG
      if  request.POST['article_slug']!="blabla":
        article = Article.objects.get(slug=request.POST['article_slug'])

        #save the comment in the table and get all comments related to the article
        c = Comment(writer=inscrit, comment_content=content, commented_article=article)
        c.save()

        return redirect(f"/articles/{article.slug}")

      else:
        c = Comment(writer=inscrit, comment_content=content)
        c.save()
        return render(request, 'learning/welcome.html', {'comment_report':'Commentaire envoyé avec succès!'})

    else:
      return render(request, 'learning/welcome.html', {'comment_failure':"Echec d'envoi!"})

  else:
    return redirect('home')



#to access the form designed to send a reply
def reply_view(request, comment_token):
  if request.user.is_authenticated:
    comment = Comment.objects.get(comment_token=comment_token)
    return render(request, 'articles/reply.html', {'comment':comment})
  else:
    return redirect('login')

#insertion d'une reponse
def replying_view(request):

  comment = Comment.objects.get(pk=request.POST.get('comment_id'))
  if not request.user.is_authenticated:
      return redirect('login')

  if request.method == "POST":
    f = ReplyForm(request.POST)
    if f.is_valid():
      replier = get_object_or_404(User, pk=request.user.id)
      reply_content = f.cleaned_data['reply_content']

      reply = Comment(writer=replier, comment_content=reply_content, commented_article=comment.commented_article, parent=comment)
      reply.save()

      return redirect(f"/articles/comment/replies/{comment.comment_token}")
    else:
      return render(request, 'articles/replies.html', {'comment':comment, 'replies':comment.replies, 'authen':'Réponse invalide!'})
  else:
    return redirect('/articles/')


#pour voir les reponses à un commentaire
def comment_replies_view(request, comment_token):

  try:
    comment = Comment.objects.get(comment_token = comment_token)
  except:
    return redirect('/articles/')

  #get all replies related to the comment
  comment_replies = comment.replies

  return render(request, 'articles/replies.html', {'replies':comment_replies, 'comment':comment})

def delete_comment_view(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    article = Article.objects.get(pk=comment.commented_article.id)
    comment.delete()

    return redirect(f"/articles/{article.slug}")



def delete_reply_view(request, reply_id):
    reply = Comment.objects.get(pk=reply_id)
    reply.delete()
    return redirect(f"/articles/comment/replies/{reply.comment_token}")

# End
# End
# End
# End
