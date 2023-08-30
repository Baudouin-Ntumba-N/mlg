
from articles import views
from django.contrib import admin
from django.urls import path

urlpatterns = [

    path('articles/', views.articles_list_view, name='articles'),
    path('articles/<str:slug>', views.article_details_view, name='article-details'),
    path('articles/create/', views.create_article_view, name='create-article'),
    path('articles/update/<str:slug>', views.update_article_view, name="update-article"),
    path('articles/comment/', views.comment_view, name='comment'),
    path('articles/comment/reply/<str:token>', views.reply_view, name='reply'),
    path('articles/comment/replying', views.replying_view, name='replying'),
    path('articles/comment/replies/<str:token>', views.comment_replies_view, name='comment-replies') ,
    path('articles/comment/delete/<int:comment_id>', views.delete_comment_view, name='delete-comment'),
    path('articles/comment/reply/delete/<int:reply_id>', views.delete_reply_view, name='delete-reply'),
    path('article/like/<str:article_slug>', views.like_article, name='like-article'),

    path('articles-api/', views.article_list, name='articles-api'),
    path('articles-api/<int:pk>', views.article_detail, name='api-article-detail'),


]