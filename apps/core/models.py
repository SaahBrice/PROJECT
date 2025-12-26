"""
Core App Models
Site-wide settings, team members, testimonials, and partners.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """
    Singleton model for site-wide settings.
    Only one instance should exist.
    """
    
    # Basic Info
    site_name = models.CharField(_("Nom du site"), max_length=100, default="FDTM")
    tagline = models.CharField(_("Slogan"), max_length=200, 
                               default="Construire un avenir plus lumineux, main dans la main")
    
    # Content
    about_text = models.TextField(_("Texte À propos"), blank=True)
    mission_text = models.TextField(_("Texte Mission"), blank=True)
    vision_text = models.TextField(_("Texte Vision"), blank=True)
    
    # Contact
    contact_email = models.EmailField(_("Email de contact"), default="contact@fdtm.org")
    contact_phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    address = models.TextField(_("Adresse"), blank=True)
    
    # Social Links (JSON)
    social_links = models.JSONField(_("Liens sociaux"), default=dict, blank=True,
                                    help_text=_('Ex: {"facebook": "url", "instagram": "url"}'))
    
    # Footer
    footer_text = models.TextField(_("Texte du pied de page"), blank=True)
    
    # SEO
    default_meta_description = models.CharField(_("Meta description par défaut"), 
                                                max_length=160, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(_("ID Google Analytics"), max_length=50, blank=True)
    
    class Meta:
        verbose_name = _("Paramètres du site")
        verbose_name_plural = _("Paramètres du site")
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create the singleton instance"""
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings


class TeamMember(models.Model):
    """Team members - founders, staff, volunteers"""
    
    class Role(models.TextChoices):
        FOUNDER = 'founder', _('Fondateur')
        BOARD = 'board', _('Conseil d\'administration')
        STAFF = 'staff', _('Personnel')
        VOLUNTEER = 'volunteer', _('Bénévole')
        PARTNER = 'partner', _('Partenaire')
    
    name = models.CharField(_("Nom"), max_length=100)
    role = models.CharField(_("Rôle"), max_length=20, choices=Role.choices, default=Role.STAFF)
    title = models.CharField(_("Titre/Fonction"), max_length=100)
    bio = models.TextField(_("Biographie"), blank=True)
    photo = models.ImageField(_("Photo"), upload_to='team/', blank=True)
    photo_url = models.URLField(_("URL photo"), blank=True)
    
    # Contact
    email = models.EmailField(_("Email"), blank=True)
    linkedin_url = models.URLField(_("LinkedIn"), blank=True)
    
    # Display
    is_active = models.BooleanField(_("Actif"), default=True)
    order = models.PositiveIntegerField(_("Ordre d'affichage"), default=0)
    show_on_homepage = models.BooleanField(_("Afficher sur l'accueil"), default=False)
    
    class Meta:
        verbose_name = _("Membre de l'équipe")
        verbose_name_plural = _("Membres de l'équipe")
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.title}"


class Testimonial(models.Model):
    """Testimonials from beneficiaries, donors, or partners"""
    
    class Type(models.TextChoices):
        BENEFICIARY = 'beneficiary', _('Bénéficiaire')
        DONOR = 'donor', _('Donateur')
        PARTNER = 'partner', _('Partenaire')
        VOLUNTEER = 'volunteer', _('Bénévole')
    
    name = models.CharField(_("Nom"), max_length=100)
    type = models.CharField(_("Type"), max_length=20, choices=Type.choices, 
                           default=Type.BENEFICIARY)
    location = models.CharField(_("Lieu"), max_length=100, blank=True)
    quote = models.TextField(_("Témoignage"))
    photo = models.ImageField(_("Photo"), upload_to='testimonials/', blank=True)
    
    # Association
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Projet"),
        related_name='testimonials'
    )
    
    # Display
    is_featured = models.BooleanField(_("Mis en avant"), default=False)
    is_active = models.BooleanField(_("Actif"), default=True)
    
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"


class Partner(models.Model):
    """Partner organizations, sponsors, and supporters"""
    
    class Type(models.TextChoices):
        SPONSOR = 'sponsor', _('Sponsor')
        PARTNER = 'partner', _('Partenaire')
        SUPPORTER = 'supporter', _('Soutien')
        MEDIA = 'media', _('Média')
    
    name = models.CharField(_("Nom"), max_length=200)
    type = models.CharField(_("Type"), max_length=20, choices=Type.choices)
    logo = models.ImageField(_("Logo"), upload_to='partners/')
    website = models.URLField(_("Site web"), blank=True)
    description = models.TextField(_("Description"), blank=True)
    
    is_active = models.BooleanField(_("Actif"), default=True)
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    
    class Meta:
        verbose_name = _("Partenaire")
        verbose_name_plural = _("Partenaires")
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ImpactStat(models.Model):
    """Impact statistics for display on homepage and about page"""
    
    title = models.CharField(_("Titre"), max_length=100)
    value = models.CharField(_("Valeur"), max_length=50,
                            help_text=_("Ex: 500+, 10000, 25"))
    suffix = models.CharField(_("Suffixe"), max_length=50, blank=True,
                             help_text=_("Ex: familles, élèves, projets"))
    icon = models.CharField(_("Icône"), max_length=50, blank=True)
    
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    is_active = models.BooleanField(_("Actif"), default=True)
    
    class Meta:
        verbose_name = _("Statistique d'impact")
        verbose_name_plural = _("Statistiques d'impact")
        ordering = ['order']
    
    def __str__(self):
        return f"{self.title}: {self.value}"


class FAQ(models.Model):
    """Frequently Asked Questions"""
    
    question = models.CharField(_("Question"), max_length=300)
    answer = models.TextField(_("Réponse"))
    
    category = models.CharField(_("Catégorie"), max_length=100, blank=True,
                               help_text=_("Ex: Dons, Projets, Général"))
    
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    is_active = models.BooleanField(_("Actif"), default=True)
    
    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['order']
    
    def __str__(self):
        return self.question[:50]


class ContactMessage(models.Model):
    """Contact form submissions"""
    
    name = models.CharField(_("Nom"), max_length=100)
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    subject = models.CharField(_("Sujet"), max_length=200)
    message = models.TextField(_("Message"))
    
    # Status
    is_read = models.BooleanField(_("Lu"), default=False)
    is_replied = models.BooleanField(_("Répondu"), default=False)
    
    # Metadata
    ip_address = models.GenericIPAddressField(_("Adresse IP"), null=True, blank=True)
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    """Newsletter subscribers"""
    
    email = models.EmailField(_("Email"), unique=True)
    name = models.CharField(_("Nom"), max_length=100, blank=True)
    
    is_active = models.BooleanField(_("Actif"), default=True)
    subscribed_at = models.DateTimeField(_("Inscrit le"), auto_now_add=True)
    unsubscribed_at = models.DateTimeField(_("Désinscrit le"), null=True, blank=True)
    
    # Preferences
    language = models.CharField(_("Langue préférée"), max_length=2, default='fr')
    
    class Meta:
        verbose_name = _("Abonné newsletter")
        verbose_name_plural = _("Abonnés newsletter")
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email


class Event(models.Model):
    """Upcoming events - conferences, festivals, community gatherings"""
    
    title = models.CharField(_("Titre"), max_length=200)
    description = models.TextField(_("Description"))
    short_description = models.CharField(_("Description courte"), max_length=300, blank=True)
    
    # Date and time
    event_date = models.DateTimeField(_("Date de l'événement"))
    end_date = models.DateTimeField(_("Date de fin"), null=True, blank=True)
    
    # Location
    location = models.CharField(_("Lieu"), max_length=200)
    address = models.TextField(_("Adresse complète"), blank=True)
    
    # Media
    image = models.ImageField(_("Image"), upload_to='events/', blank=True)
    image_url = models.URLField(_("URL image"), blank=True)
    
    # Status
    is_featured = models.BooleanField(_("Mis en avant"), default=False)
    is_published = models.BooleanField(_("Publié"), default=True)
    
    # Link to project (optional)
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        verbose_name=_("Projet associé")
    )
    
    # Timestamps
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modifié le"), auto_now=True)
    
    class Meta:
        verbose_name = _("Événement")
        verbose_name_plural = _("Événements")
        ordering = ['event_date']
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        from django.utils import timezone
        return self.event_date > timezone.now()
    
    @property
    def days_until(self):
        from django.utils import timezone
        if self.is_upcoming:
            delta = self.event_date - timezone.now()
            return delta.days
        return 0
