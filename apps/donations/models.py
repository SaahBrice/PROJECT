"""
Donations App Models
Handles financial donations and material contributions.
Supports multiple payment methods (Stripe, Fapshi) and tracks donation status.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


class Donation(models.Model):
    """
    Financial donation model.
    Can be linked to a specific project or be general (where most needed).
    """
    
    class PaymentMethod(models.TextChoices):
        STRIPE = 'stripe', 'Stripe'
        FAPSHI = 'fapshi', 'Fapshi'
        BANK_TRANSFER = 'bank', _('Virement bancaire')
        OTHER = 'other', _('Autre')
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('En attente')
        PROCESSING = 'processing', _('En cours')
        COMPLETED = 'completed', _('Complété')
        FAILED = 'failed', _('Échoué')
        REFUNDED = 'refunded', _('Remboursé')
        CANCELLED = 'cancelled', _('Annulé')
    
    class Currency(models.TextChoices):
        EUR = 'EUR', 'Euro (€)'
        USD = 'USD', 'US Dollar ($)'
        XAF = 'XAF', 'CFA Franc (FCFA)'
        GBP = 'GBP', 'British Pound (£)'
    
    # Unique identifier
    reference = models.UUIDField(_("Référence"), default=uuid.uuid4, unique=True, editable=False)
    
    # Donor Info
    donor_name = models.CharField(_("Nom du donateur"), max_length=200)
    donor_email = models.EmailField(_("Email du donateur"))
    donor_phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    is_anonymous = models.BooleanField(_("Don anonyme"), default=False,
                                       help_text=_("Ne pas afficher le nom publiquement"))
    
    # Amount
    amount = models.DecimalField(_("Montant"), max_digits=12, decimal_places=2)
    currency = models.CharField(_("Devise"), max_length=3, choices=Currency.choices, default=Currency.EUR)
    
    # Project Association
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Projet"),
        related_name='donations',
        help_text=_("Laissez vide pour un don général")
    )
    project_need = models.ForeignKey(
        'projects.ProjectNeed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Besoin spécifique"),
        related_name='donations'
    )
    
    # Payment Info
    payment_method = models.CharField(_("Méthode de paiement"), max_length=20, 
                                      choices=PaymentMethod.choices)
    status = models.CharField(_("Statut"), max_length=20, choices=Status.choices, 
                             default=Status.PENDING)
    
    # Payment Gateway IDs
    stripe_payment_intent_id = models.CharField(_("Stripe Payment Intent ID"), 
                                                max_length=100, blank=True)
    stripe_session_id = models.CharField(_("Stripe Session ID"), max_length=100, blank=True)
    fapshi_transaction_id = models.CharField(_("Fapshi Transaction ID"), max_length=100, blank=True)
    
    # Message
    message = models.TextField(_("Message du donateur"), blank=True,
                              help_text=_("Message optionnel du donateur"))
    
    # Metadata
    ip_address = models.GenericIPAddressField(_("Adresse IP"), null=True, blank=True)
    user_agent = models.TextField(_("User Agent"), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    completed_at = models.DateTimeField(_("Complété le"), null=True, blank=True)
    
    # Email flags
    receipt_sent = models.BooleanField(_("Reçu envoyé"), default=False)
    thank_you_sent = models.BooleanField(_("Remerciement envoyé"), default=False)
    
    class Meta:
        verbose_name = _("Don")
        verbose_name_plural = _("Dons")
        ordering = ['-created_at']
    
    def __str__(self):
        project_name = self.project.title if self.project else _("Général")
        return f"{self.donor_name} - {self.amount} {self.currency} - {project_name}"
    
    def mark_completed(self):
        """Mark donation as completed and update project funding"""
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save()
        
        # Update project current_amount
        if self.project:
            self.project.current_amount += self.amount
            self.project.save(update_fields=['current_amount'])
            
            # Update specific need if applicable
            if self.project_need:
                self.project_need.current_amount += self.amount
                self.project_need.save(update_fields=['current_amount'])
    
    @property
    def display_name(self):
        """Return display name (anonymous or real name)"""
        if self.is_anonymous:
            return _("Donateur anonyme")
        return self.donor_name
    
    @property
    def formatted_amount(self):
        """Return formatted amount with currency symbol"""
        symbols = {'EUR': '€', 'USD': '$', 'XAF': 'FCFA', 'GBP': '£'}
        symbol = symbols.get(self.currency, self.currency)
        return f"{self.amount:,.2f} {symbol}"


class MaterialContribution(models.Model):
    """
    Material/in-kind contribution pledges.
    Tracks pledges for material needs in projects.
    """
    
    class Status(models.TextChoices):
        PLEDGED = 'pledged', _('Promis')
        CONFIRMED = 'confirmed', _('Confirmé')
        DELIVERED = 'delivered', _('Livré')
        CANCELLED = 'cancelled', _('Annulé')
    
    # Reference
    reference = models.UUIDField(_("Référence"), default=uuid.uuid4, unique=True, editable=False)
    
    # Contributor Info
    contributor_name = models.CharField(_("Nom du contributeur"), max_length=200)
    contributor_email = models.EmailField(_("Email"))
    contributor_phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    
    # Project Need
    project_need = models.ForeignKey(
        'projects.ProjectNeed',
        on_delete=models.CASCADE,
        verbose_name=_("Besoin du projet"),
        related_name='material_contributions'
    )
    
    # Contribution Details
    description = models.TextField(_("Description de la contribution"))
    quantity = models.PositiveIntegerField(_("Quantité"), default=1)
    estimated_value = models.DecimalField(_("Valeur estimée"), max_digits=10, decimal_places=2,
                                         null=True, blank=True)
    
    # Status
    status = models.CharField(_("Statut"), max_length=20, choices=Status.choices, 
                             default=Status.PLEDGED)
    
    # Delivery Info
    delivery_date = models.DateField(_("Date de livraison prévue"), null=True, blank=True)
    delivery_notes = models.TextField(_("Notes de livraison"), blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_("Créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Modifié le"), auto_now=True)
    
    class Meta:
        verbose_name = _("Contribution matérielle")
        verbose_name_plural = _("Contributions matérielles")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.contributor_name} - {self.project_need.title}"
    
    def mark_delivered(self):
        """Mark contribution as delivered and update project need"""
        self.status = self.Status.DELIVERED
        self.save()
        
        # Update the project need quantity received
        self.project_need.quantity_received += self.quantity
        self.project_need.save(update_fields=['quantity_received'])


class DonationImpact(models.Model):
    """
    Define what different donation amounts can achieve.
    Used to show donors the impact of their contribution.
    """
    
    amount = models.DecimalField(_("Montant"), max_digits=10, decimal_places=2)
    currency = models.CharField(_("Devise"), max_length=3, default='EUR')
    description = models.TextField(_("Description de l'impact"))
    icon = models.CharField(_("Icône"), max_length=50, blank=True)
    
    # Visual story fields
    image = models.ImageField(_("Image"), upload_to='donations/impact/', blank=True, null=True,
                              help_text=_("Photo illustrant l'impact (ex: bénéficiaire)"))
    short_story = models.CharField(_("Courte histoire"), max_length=200, blank=True,
                                   help_text=_("Ex: Marie a reçu ses fournitures scolaires grâce aux donateurs"))
    is_featured = models.BooleanField(_("Mis en avant"), default=False,
                                      help_text=_("Afficher en priorité sur la page de dons"))
    
    # Optional: link to specific project category
    project_category = models.ForeignKey(
        'projects.ProjectCategory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Catégorie de projet")
    )
    
    order = models.PositiveIntegerField(_("Ordre"), default=0)
    
    class Meta:
        verbose_name = _("Impact de don")
        verbose_name_plural = _("Impacts de dons")
        ordering = ['order', 'amount']
    
    def __str__(self):
        return f"{self.amount} {self.currency} - {self.description[:50]}"

