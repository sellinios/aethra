from rest_framework.generics import ListAPIView, RetrieveAPIView
from articles.models import ArticlesArticle
from api.serializers.serializer_articles import ArticlesArticleSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import os


# List all articles (ListAPIView)
class ArticlesArticleListView(ListAPIView):
    serializer_class = ArticlesArticleSerializer
    permission_classes = [AllowAny]

    # Override the default queryset to filter out future-dated articles and unpublished articles
    def get_queryset(self):
        return ArticlesArticle.objects.filter(
            published_date__lte=timezone.now().date(),  # Use published_date instead of date
            published=True  # Only published articles
        ).order_by('-published_date')  # Order by published_date, newest first


# Detail view for a single article by slug (RetrieveAPIView)
class ArticlesArticleDetailView(RetrieveAPIView):
    serializer_class = ArticlesArticleSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

    # Override the default queryset to filter out future-dated articles and unpublished articles
    def get_queryset(self):
        return ArticlesArticle.objects.filter(
            published_date__lte=timezone.now().date(),  # Use published_date instead of date
            published=True  # Only published articles
        )


# Upload file view for TinyMCE
@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_name = default_storage.save(os.path.join('articles_images/', upload.name), ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'url': file_url
        })
    return JsonResponse({
        'error': 'No file was uploaded.'
    })