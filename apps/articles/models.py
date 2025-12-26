"""
Articles App Models
Handles articles/blog posts that can be linked to projects or be global.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class ArticleCategory(models.Model):
    """Categories for articles: News, Stories, Reports, etc."""
    
    name = models.CharField(_("Nom"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    
    class Meta:
        verbose_name = _("Catégorie d'article")
        verbose_name_plural = _("Catégories d'articles")
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """
    Article/Blog post model.
    Can be linked to specific projects or be global (all projects).
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Brouillon')
        PUBLISHED = 'published', _('Publié')
        ARCHIVED = 'archived', _('Archivé')
    
    # Basic Info
    title = models.CharField(_("Titre"), max_length=250)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, max_length=280)
    
    # Content
    excerpt = models.TextField(_("Extrait"), max_length=400,
                              help_text=_("Résumé affiché dans les listes"))
    content = models.TextField(_("Contenu"))
    
    # Media
    featured_image = models.ImageField(_("Image principale"), upload_to='articles/featured/', blank=True)
    featured_image_url = models.URLField(_("URL image externe"), blank=True,
                                         help_text=_("Utilisez une URL si pas d'image uploadée"))
    image_caption = models.CharField(_("Légende de l'image"), max_length=200, blank=True)
    reading_time = models.PositiveIntegerField(_("Temps de lecture (min)"), default=3)
    
    # Categorization
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Catégorie"),
        related_name='articles'
    )
    
    # Project Association
    projects = models.ManyToManyField(
        'projects.Project',
        blank=True,
        verbose_name=_("Projets associés"),
        related_name='articles',
        help_text=_("Laissez vide pour un article global")
    )
    is_global = models.BooleanField(
        _("Article global"),
        default=False,
        help_text=_("Cochez si cet article concerne tous les projets")
    )
    
    # Author (optional - for volunteer/guest writers)
    author_name = models.CharField(_("Nom de l'auteur"), max_length=100, blank=True)
    author_bio = models.TextField(_("Bio de l'auteur"), blank=True, max_length=300)
    author_photo = models.ImageField(_("Photo de l'auteur"), upload_to='articles/authors/', 
                                     blank=True)
    
    # Status & Dates
    status = models.CharField(_("Statut"), max_length=20, choices=Status.choices, 
                             default=Status.DRAFT)
    is_featured = models.BooleanField(_("Mis en avant"), default=False)
    published_date = models.DateTimeField(_("Date de publication"), null=True, blank=True)
    
    # Engagement
    views_count = models.PositiveIntegerField(_("Nombre de vues"), default=0)
    
    # SEO
    meta_title = models.CharField(_("Titre SEO"), max_length=70, blank=True)
    meta_description = models.CharField(_("Description SEO"), max_length=160, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modifié le"), auto_now=True)
    
    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['-is_featured', '-published_date']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Auto-set SEO fields if empty
        if not self.meta_title:
            self.meta_title = self.title[:70]
        if not self.meta_description:
            self.meta_description = self.excerpt[:160]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})
    
    def increment_views(self):
        """Increment view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])


class ArticleImage(models.Model):
    """
    Additional images for articles (gallery).
    """
    
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='gallery_images',
        verbose_name=_("Article")
    )
    image = models.ImageField(_("Image"), upload_to='articles/gallery/')
    caption = models.CharField(_("Légende"), max_length=200, blank=True)
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    
    class Meta:
        verbose_name = _("Image d'article")
        verbose_name_plural = _("Images d'articles")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.article.title} - Image {self.order}"
