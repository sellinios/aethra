from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE  # Import TinyMCE widget
from .models import ArticlesArticle, ArticlesCategory

# Create a custom form to use TinyMCE for the 'content' field
class ArticlesArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = ArticlesArticle
        fields = '__all__'  # Make sure all fields including 'slug' are included

# Register ArticlesArticleAdmin with the custom form
@admin.register(ArticlesArticle)
class ArticlesArticleAdmin(admin.ModelAdmin):
    form = ArticlesArticleAdminForm
    list_display = ('title', 'author', 'category', 'get_published_date', 'get_created_at', 'published')
    search_fields = ('title', 'author__username')
    list_filter = ('category', 'created_at', 'published_date', 'published')
    prepopulated_fields = {'slug': ('title',)}  # Ensure slug is prepopulated from title
    ordering = ['-published_date']  # Order by published_date, newest first

    # Customize the fieldsets to include the meta tags
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'content', 'image', 'published', 'published_date')  # Added 'slug' here
        }),
        ('SEO Meta Tags', {  # Add this section for meta tags
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
    )

    # Customize date format for 'published_date'
    def get_published_date(self, obj):
        return obj.published_date.strftime('%d-%m-%Y')

    get_published_date.admin_order_field = 'published_date'
    get_published_date.short_description = 'Published Date'

    # Customize date format for 'created_at'
    def get_created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M')

    get_created_at.admin_order_field = 'created_at'
    get_created_at.short_description = 'Created At'

@admin.register(ArticlesCategory)
class ArticlesCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
