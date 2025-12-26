"""
Projects App Models
Handles projects with funding goals, needs (financial & material), and updates.
"""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class ProjectCategory(models.Model):
    """Categories for projects: Health, Education, Culture, Humanitarian Aid"""
    
    name = models.CharField(_("Nom"), max_length=100)
    slug = models.SlugField(_("Slug"), unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    icon = models.CharField(_("Icône"), max_length=50, blank=True, 
                           help_text=_("Nom de l'icône (ex: heart, book, globe)"))
    color = models.CharField(_("Couleur"), max_length=20, default="#C75B2A",
                            help_text=_("Code couleur hexadécimal"))
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    
    class Meta:
        verbose_name = _("Catégorie de projet")
        verbose_name_plural = _("Catégories de projets")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    """
    Main project model with funding goals and tracking.
    Projects can have multiple needs (financial & material).
    """
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Brouillon')
        ACTIVE = 'active', _('Actif')
        FUNDED = 'funded', _('Financé')
        COMPLETED = 'completed', _('Terminé')
        PAUSED = 'paused', _('En pause')
    
    # Basic Info
    title = models.CharField(_("Titre"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True, blank=True, max_length=250)
    category = models.ForeignKey(
        ProjectCategory, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name=_("Catégorie"),
        related_name='projects'
    )
    
    # Content
    short_description = models.TextField(_("Description courte"), max_length=300,
                                        help_text=_("Affichée dans les listes et cartes"))
    description = models.TextField(_("Description complète"))
    impact_description = models.TextField(_("Impact attendu"), blank=True,
                                         help_text=_("Décrivez l'impact de ce projet"))
    
    # Media
    featured_image = models.ImageField(_("Image principale"), upload_to='projects/featured/', blank=True)
    featured_image_url = models.URLField(_("URL image externe"), blank=True,
                                         help_text=_("Utilisez une URL si pas d'image uploadée"))
    gallery_images = models.JSONField(_("Galerie d'images"), default=list, blank=True,
                                      help_text=_("Liste des URLs d'images"))
    video_url = models.URLField(_("URL vidéo"), blank=True)
    
    # Location
    location = models.CharField(_("Lieu"), max_length=200, default="Dschang, Cameroun")
    location_coordinates = models.CharField(_("Coordonnées GPS"), max_length=100, blank=True)
    
    # Funding
    goal_amount = models.DecimalField(_("Objectif financier"), max_digits=12, decimal_places=2, default=0)
    current_amount = models.DecimalField(_("Montant actuel"), max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(_("Devise"), max_length=3, default='EUR')
    
    # Status & Dates
    status = models.CharField(_("Statut"), max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(_("Mis en avant"), default=False)
    is_urgent = models.BooleanField(_("Urgent"), default=False)
    start_date = models.DateField(_("Date de début"), null=True, blank=True)
    end_date = models.DateField(_("Date de fin prévue"), null=True, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modifié le"), auto_now=True)
    
    class Meta:
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")
        ordering = ['-is_featured', '-is_urgent', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    @property
    def progress_percentage(self):
        """Calculate funding progress percentage"""
        if self.goal_amount <= 0:
            return 0
        percentage = (self.current_amount / self.goal_amount) * 100
        return min(percentage, 100)  # Cap at 100%
    
    @property
    def amount_remaining(self):
        """Calculate remaining amount to reach goal"""
        remaining = self.goal_amount - self.current_amount
        return max(remaining, 0)
    
    @property
    def is_fully_funded(self):
        """Check if project has reached its funding goal"""
        return self.current_amount >= self.goal_amount
    
    @property
    def total_donors(self):
        """Count unique donors for this project"""
        return self.donations.filter(status='completed').values('donor_email').distinct().count()


class ProjectNeed(models.Model):
    """
    Specific needs for a project - can be financial or material.
    Allows donors to contribute to specific aspects of a project.
    """
    
    class NeedType(models.TextChoices):
        FINANCIAL = 'financial', _('Financier')
        MATERIAL = 'material', _('Matériel')
    
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE,
        related_name='needs',
        verbose_name=_("Projet")
    )
    need_type = models.CharField(_("Type de besoin"), max_length=20, choices=NeedType.choices)
    
    # For all needs
    title = models.CharField(_("Titre"), max_length=200)
    description = models.TextField(_("Description"))
    
    # For financial needs
    target_amount = models.DecimalField(_("Montant cible"), max_digits=10, decimal_places=2, 
                                        null=True, blank=True)
    current_amount = models.DecimalField(_("Montant actuel"), max_digits=10, decimal_places=2, 
                                         default=0)
    
    # For material needs
    item_name = models.CharField(_("Nom de l'article"), max_length=200, blank=True)
    quantity_needed = models.PositiveIntegerField(_("Quantité nécessaire"), default=0)
    quantity_received = models.PositiveIntegerField(_("Quantité reçue"), default=0)
    unit = models.CharField(_("Unité"), max_length=50, blank=True,
                           help_text=_("Ex: pièces, kg, boîtes"))
    
    # Status
    is_fulfilled = models.BooleanField(_("Accompli"), default=False)
    priority = models.PositiveSmallIntegerField(_("Priorité"), default=1,
                                                help_text=_("1 = haute priorité"))
    
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Besoin du projet")
        verbose_name_plural = _("Besoins des projets")
        ordering = ['priority', '-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"
    
    @property
    def progress_percentage(self):
        """Calculate progress for financial needs"""
        if self.need_type == self.NeedType.FINANCIAL and self.target_amount:
            if self.target_amount <= 0:
                return 0
            return min((self.current_amount / self.target_amount) * 100, 100)
        elif self.need_type == self.NeedType.MATERIAL and self.quantity_needed:
            if self.quantity_needed <= 0:
                return 0
            return min((self.quantity_received / self.quantity_needed) * 100, 100)
        return 0


class ProjectUpdate(models.Model):
    """
    Updates/news about a project's progress.
    Shows donors and visitors how the project is evolving.
    """
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='updates',
        verbose_name=_("Projet")
    )
    title = models.CharField(_("Titre"), max_length=200)
    content = models.TextField(_("Contenu"))
    image = models.ImageField(_("Image"), upload_to='projects/updates/', blank=True)
    
    is_milestone = models.BooleanField(_("Jalon important"), default=False,
                                       help_text=_("Marquer comme étape importante"))
    
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Mise à jour du projet")
        verbose_name_plural = _("Mises à jour des projets")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"
