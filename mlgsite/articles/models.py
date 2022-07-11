from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from learning.models import Categorie, Inscrit
from django.template.defaultfilters import slugify




User = get_user_model()


class Article(models.Model):

  title = models.CharField(max_length=100)

  categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)

  slug = models.SlugField(max_length=255, unique=True, blank=True)

  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  updated_on = models.DateTimeField(auto_now=True)

  content = models.TextField(blank=True, verbose_name='Contenu')

  photo = models.ImageField(null=True, upload_to='images')

  pub_date = models.DateTimeField(null=True)

  published = models.BooleanField(default=False)

  def __str__(self):
    return self.title

  #methode save() modifiée
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)

class Reponse(models.Model):
    replier = models.ForeignKey(Inscrit, on_delete=models.CASCADE, null=True)
    reply_recipient = models.ForeignKey(Inscrit, on_delete=models.CASCADE, null=True, related_name='reply_recipient')
    reply_content = models.TextField(null=True, blank=True)
    related_comment_id = models.IntegerField(null=True)
    reply_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
      return self.reply_content


class Comment(models.Model):

    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    comment_content = models.TextField(blank=True, verbose_name='Commentaire')

    commented_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    replies = models.ManyToManyField(Reponse)

    post_date = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
      return str(self.id)

    def delele(self, *args, **kwargs):
      for reply in self.replies.all():
        reponse = Reponse.objects.get(pk=reply.id)
        reponse.delete()
      super().delete(*args, **kwargs)



class CommentAdmin(admin.ModelAdmin):

  list_display=('id', 'writer', 'comment_content', 'commented_article', 'post_date')

  list_filter =('writer',)



class ReponseAdmin(admin.ModelAdmin):
  list_display = ('id', 'replier', 'reply_recipient', 'reply_content', 'related_comment_id', 'reply_date')
  list_filter = ('id', 'replier', 'reply_recipient', 'reply_content', 'related_comment_id', 'reply_date')