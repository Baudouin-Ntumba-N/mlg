from django import forms
from .models import Article




class ArticleForm(forms.ModelForm):

  class Meta:
    model = Article
    fields = ["id", "title", "categorie", "author", "content", "photo", "published"]

class UpdateArticleForm(forms.ModelForm):

  class Meta:
    model = Article
    fields = ["id", "title", "categorie", "author", "content", "photo", "published"]







class ReplyForm(forms.Form):

  reply_content = forms.CharField(widget = forms.TextInput())

  comment_id = forms.CharField(widget = forms.HiddenInput())

class CommentForm(forms.Form):

  #user_id = forms.CharField(widget = forms.HiddenInput())

  article_slug = forms.CharField(widget = forms.HiddenInput())

  content = forms.CharField(widget = forms.TextInput())