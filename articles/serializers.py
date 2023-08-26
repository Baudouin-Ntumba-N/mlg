from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model
from learning.models import Categorie

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'photo')


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ('id', 'nom')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False)
    categorie = CategorieSerializer(many=False)

    class Meta:
        model = Article
        # fields = ['id', 'title', 'categorie'', 'author', 'content', 'pub_date', 'photo']
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    commented_article = ArticleSerializer(many=False)
    writer = UserSerializer(many=False)

    class Meta:
        model = Comment
        fields = "__all__"


class CommentSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'writer', 'comment_content', 'commented_article')
