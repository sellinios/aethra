# api/serializers/serializer_articles.py

from rest_framework import serializers
from articles.models import ArticlesArticle

class ArticlesArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticlesArticle
        fields = [
            'id',
            'title',
            'author',
            'content',
            'slug',
            'created_at',
            'published_date',
            'category',
            'image',
            'meta_title',
            'meta_description',
            'meta_keywords',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        content = representation.get('content', '')
        print('Serializer content:', content)  # For debugging
        return representation
