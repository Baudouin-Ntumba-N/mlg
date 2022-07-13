from django.contrib import admin
from articles.models import Article, Comment, CommentAdmin, Reponse, ReponseAdmin
admin.site.register(Article)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reponse, ReponseAdmin)