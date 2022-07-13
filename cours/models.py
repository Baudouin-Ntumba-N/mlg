from django.db import models
from django.contrib import admin
from django.template.defaultfilters import slugify
from articles.models import Categorie
# Create your models here.

class EnglishLesson(models.Model):
  title = models.CharField(max_length=100, null=False)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  content = models.TextField(blank=True)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)




class MathLesson(models.Model):
  title = models.CharField(max_length=100, null=False)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  content = models.TextField(blank=True)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)

class GeoscienceLesson(models.Model):
  title = models.CharField(max_length=100, null=False)
  slug = models.SlugField(max_length=255, unique=True, blank=True)
  content = models.TextField(blank=True)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)
  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)


class Videolesson(models.Model):
  title = models.CharField(max_length=100, null=False)
  slug = models.SlugField(max_length=200, unique=True, blank=True)
  categorie = models.ForeignKey(Categorie, on_delete = models.SET_NULL, null=True, blank=True)
  video_file = models.FileField(upload_to ='videos', null=False)


  def save(self, *args, **kwargs):
    if not self.slug:
      self.slug = slugify(self.title)
      super().save(*args, **kwargs)
    else:
      super().save(*args, **kwargs)

  class Meta:
    verbose_name = "Leçons vidéo"


class VideolessonAdmin(admin.ModelAdmin):

  list_display = ('id', 'title', 'categorie' )
  list_filter = ('categorie',)