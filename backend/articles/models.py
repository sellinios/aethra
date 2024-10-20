from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings  # Correct import for the user model

class ArticlesCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'articles_category'
        verbose_name_plural = "Categories"
        managed = True


class ArticlesArticle(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = HTMLField('Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateField()  # Renamed from 'date' to 'published_date'
    image = models.ImageField(upload_to='articles_images/', blank=True, null=True)
    published = models.BooleanField(default=False)
    category = models.ForeignKey(ArticlesCategory, related_name='articles', on_delete=models.CASCADE)

    # New Meta Tag fields for SEO
    meta_title = models.CharField(max_length=255, blank=True, null=True)  # Meta Title
    meta_description = models.TextField(blank=True, null=True)  # Meta Description
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)  # Meta Keywords

    def save(self, *args, **kwargs):
        # Automatically set to unpublished if the published_date is in the future
        if self.published_date > timezone.now().date():
            self.published = False
        if not self.slug:
            self.slug = slugify(self.title)[:255]
            original_slug = self.slug
            counter = 1
            while ArticlesArticle.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                if len(self.slug) > 255:
                    self.slug = self.slug[:255 - len(str(counter)) - 1]
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'articles_article'
        verbose_name_plural = "Articles"
        managed = True
        ordering = ['-published_date']  # Order by published_date, newest first
