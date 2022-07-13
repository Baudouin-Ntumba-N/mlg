from django.shortcuts import render, redirect, get_object_or_404
from articles.models import Article, Comment, Reponse
from .forms import CommentForm, ReplyForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, authenticate, login, logout



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

    comments = (Comment.objects.filter(commented_article=article)).order_by('-post_date')
    #comment_replies = Reponse.objects.all()

    return render(request, 'articles/details.html', {'article':article, 'comments':comments})




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
        return render(request, 'articles/details.html', {'article':article, 'comments':comments})

      else:
        c = Comment(writer=inscrit, comment_content=comment)
        c.save()
        return render(request, 'learning/welcome.html', {'comment_report':'Commentaire envoyé avec succès!'})

    else:
      return render(request, 'learning/welcome.html', {'comment_failure':"Echec d'envoi!"})

  else:
    return redirect('home')



#to access the form designed to send a reply
def reply_view(request, comment_id):
  if request.user.is_authenticated:
    comment = Comment.objects.get(pk=int(comment_id))
    return render(request, 'articles/reply.html', {'comment':comment})
  else:
    return redirect('login')

#insertion d'une reponse
def replying_view(request):

  that_comment = Comment.objects.get(pk=request.POST.get('comment_id'))

  if request.method == "POST":
    f = ReplyForm(request.POST)
    if f.is_valid():
      replier = get_object_or_404(User, pk=request.user.id)
      reply_recipient = User.objects.get(pk=int(request.POST['reply_recipient']))
      reply_content = f.cleaned_data['reply_content']
      related_comment_id= f.cleaned_data['comment_id']

      reply = Reponse(replier=replier, reply_recipient=reply_recipient, reply_content=reply_content, related_comment_id=related_comment_id)
      reply.save()
      comment = Comment.objects.get(pk=related_comment_id)
      comment.replies.add(reply)


      return render(request, 'articles/replies.html', {'replies':comment.replies.all(), 'comment':comment})

    else:
      return render(request, 'articles/replies.html', {'comment':that_comment, 'replies':that_comment.replies.all, 'authen':'Réponse invalide!'})
  else:
    return redirect('/articles/')


#pour voir les reponses à un commentaire
def comment_replies_view(request, comment_id):

  try:
    comment_id1 = int(comment_id)
  except:
    return redirect('/articles/')

  try:
    comment = Comment.objects.get(pk = comment_id1)
  except:
    return redirect('/articles/')
    #get all replies related to the comment
  comment_replies = comment.replies.all()

  return render(request, 'articles/replies.html', {'replies':comment_replies, 'comment':comment})


def delete_reply_view(request, reply_id):
    reply = Reponse.objects.get(pk=reply_id)
    related_comment_id = reply.related_comment_id
    reply.delete()
    comment = Comment.objects.get(pk=related_comment_id)
    comment_replies = comment.replies.all()
    context = {'replies':comment_replies, 'comment':comment}
    return render(request, 'articles/replies.html', context)