from django.contrib import admin
from .models import EnglishLesson, MathLesson, Videolesson, VideolessonAdmin, GeoscienceLesson
# Register your models here.

admin.site.register(EnglishLesson)
admin.site.register(MathLesson)
admin.site.register(Videolesson, VideolessonAdmin)
admin.site.register(GeoscienceLesson)