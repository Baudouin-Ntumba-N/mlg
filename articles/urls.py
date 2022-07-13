
from articles import views
from django.contrib import admin
from django.urls import path

urlpatterns = [

    path('articles/', views.articles_list_view, name='articles'),
    path('articles/<str:slug>', views.article_details_view, name='article-details'),
    path('articles/comment/', views.comment_view, name='comment'),
    path('articles/comment/reply/<int:comment_id>', views.reply_view, name='reply'),
    path('articles/comment/replying', views.replying_view, name='replying'),
    path('articles/comment/replies/<int:comment_id>', views.comment_replies_view, name='comment_replies') ,
    path('articles/comment/reply/delete/<int:reply_id>', views.delete_reply_view, name='delete-reply'),
]