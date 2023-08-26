
from articles import views
from django.urls import path

urlpatterns = [

    path('articles/', views.articles_list_view, name='articles'),
    path('articles/<str:slug>', views.article_details_view, name='article-details'),
    path('articles/edition/', views.edit_article_view, name='edit-article'),
    path('articles/update-article/<str:slug>', views.update_article_view, name='update-article'),
    path('articles/learning-english/articles/', views.articles_english_view, name='articles-english'),
    path('articles/apprenons-maths/articles/', views.articles_maths_view, name='articles-maths'),
    path('articles/geosciences/articles/', views.articles_geoscience_view, name='articles-geoscience'),
    path('articles/computerscience/articles/', views.articles_cs_view, name='articles-cs'),

    path('articles/comment/', views.comment_view, name='comment'),
    path('articles/comment/reply/<str:comment_token>', views.reply_view, name='reply'),
    path('articles/comment/replying', views.replying_view, name='replying'),
    path('articles/comment/replies/<str:comment_token>', views.comment_replies_view, name='comment-replies'),
    path('articles/comment/delete/<int:comment_id>', views.delete_comment_view, name='delete-comment'),
    path('articles/comment/reply/delete/<int:reply_id>', views.delete_reply_view, name='delete-reply'),


    #api urls
    path('articles-api/', views.article_list, name='articles-api'),
    path('article-api/<str:slug>/', views.article_detail,
         name='api-article-detail'),
    path('comment-api/',
         views.insert_comment, name='comment-api'),
    path('comment-replies-api/<str:parent_token>',
         views.replies_api, name='comment-api'),
    path('article-update-api/<str:slug>',
         views.article_update_detail, name='api-article-detail'),

]