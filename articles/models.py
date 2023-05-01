from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from learning.models import Categorie
from django.template.defaultfilters import slugify
from random import randrange
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField



User = get_user_model()


class Article(models.Model):

  title = models.CharField(max_length=100)

  categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, null=True)

  slug = models.SlugField(max_length=255, unique=True, blank=True)

  author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  updated_on = models.DateTimeField(auto_now=True)

  content = RichTextUploadingField(blank=True, null=True)

  photo = models.ImageField(null=True, upload_to='images')

  pub_date = models.DateTimeField(auto_now_add=True, null=True)

  published = models.BooleanField(default=False)

  def __str__(self):
    return self.title

  #methode save() modifiée
  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    elif self.slug != slugify(self.title):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)

  def get_absolute_url(self):
      return reverse("article-details", kwargs={"slug": self.slug})



class Comment(models.Model):

    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    comment_content = models.TextField(blank=True, verbose_name='Commentaire')

    commented_article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True)

    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    post_date = models.DateTimeField(auto_now_add=True, null=True)

    comment_token = models.CharField(blank=True, max_length=500)


    def __str__(self):
      return str(self.id)

    def save(self, *args, **kwargs):
      if not self.comment_token:

        the_token = f"r{ str(randrange(15)) }b{self.comment_content[0]} {len(self.writer.first_name)} {self.commented_article.slug[0]}{ str(randrange(8)) } yQ{ str(randrange(4)) }x { str(randrange(9)) } {str((self.writer.id)*34)}{ str(self.commented_article.id) }{str((self.writer.id)*4)}E { str(randrange(7)) }w"
        self.comment_token = slugify(the_token)
        super().save(*args, **kwargs)
      else:
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("comment-replies", kwargs={"comment_token": self.comment_token})

    @property
    def replies(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        else:
            return False




class CommentAdmin(admin.ModelAdmin):

  list_display=('id', 'writer', 'comment_content', 'commented_article', 'post_date')

  list_filter =('writer',)


