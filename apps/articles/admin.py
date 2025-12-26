"""
Articles Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import ArticleCategory, Article, ArticleImage


class ArticleImageInline(admin.TabularInline):
    """Inline editor for article gallery images"""
    model = ArticleImage
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'is_featured', 'is_global', 
                    'views_count', 'published_date']
    list_filter = ['status', 'category', 'is_featured', 'is_global']
    list_editable = ['is_featured']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    filter_horizontal = ['projects']
    
    inlines = [ArticleImageInline]
    
    fieldsets = (
        (_('Contenu'), {
            'fields': ('title', 'slug', 'excerpt', 'content', 'featured_image', 'image_caption')
        }),
        (_('Catégorisation'), {
            'fields': ('category', 'projects', 'is_global')
        }),
        (_('Auteur'), {
            'fields': ('author_name', 'author_bio', 'author_photo'),
            'classes': ('collapse',)
        }),
        (_('Publication'), {
            'fields': ('status', 'is_featured', 'published_date')
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Auto-set published_date when status changes to published
        if obj.status == 'published' and not obj.published_date:
            from django.utils import timezone
            obj.published_date = timezone.now()
        super().save_model(request, obj, form, change)


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    list_display = ['article', 'caption', 'order']
    list_filter = ['article']
    list_editable = ['order']
