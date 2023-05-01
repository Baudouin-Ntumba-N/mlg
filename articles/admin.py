from django.contrib import admin
from articles.models import Article, Comment, CommentAdmin
admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)
