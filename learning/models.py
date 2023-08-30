from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from learning.templatetags.learning_tags import*
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField

class AboutUs(models.Model):
    content = RichTextField(null=True)

class HomeCoverImage(models.Model):
  image = models.ImageField(upload_to = 'cover_images', default='cover_images/home.jpg', null = True)

class Inscrit(AbstractUser):
  photo = models.ImageField(upload_to = 'photos', default = 'photos/default.jpg', null = True)
  pass

class InscritAdmin(admin.ModelAdmin):
  list_display = ('id', 'username', 'first_name', 'last_name')

class Categorie(models.Model):
  nom = models.CharField(max_length=20, null=False, verbose_name='Nom')
  def __str__(self):
    return self.nom
  class Meta:
    verbose_name="Catégorie"




class Document(models.Model):

  title = models.CharField(max_length=500)

  slug = models.SlugField(unique=True, blank=True)

  document_category = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)

  doc_file = models.FileField(upload_to='documents', null=True)

  overview = models.TextField(blank=True)

  pages_number = models.IntegerField(default=0, blank=True)

  doc_format = models.CharField(max_length=10, blank=True)

  doc_size = models.CharField(max_length=10, blank=True)

  price = models.FloatField(default=0.0)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not (self.doc_format and self.doc_size and self.slug) :

      file = self.doc_file

      self.slug = slugify(self.title)

      self.doc_format = get_file_ext(file)

      self.doc_size = sizify(file.size)

      super().save(*args, **kwargs)

    else:
      super().save(*args, **kwargs)