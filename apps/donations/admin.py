"""
Donations Admin Configuration
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Donation, MaterialContribution, DonationImpact


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['reference_short', 'donor_display', 'formatted_amount', 'project_display', 
                    'payment_method', 'status_badge', 'created_at']
    list_filter = ['status', 'payment_method', 'currency', 'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'reference']
    date_hierarchy = 'created_at'
    readonly_fields = ['reference', 'stripe_payment_intent_id', 'stripe_session_id', 
                       'fapshi_transaction_id', 'created_at', 'completed_at']
    
    fieldsets = (
        (_('Référence'), {
            'fields': ('reference',)
        }),
        (_('Donateur'), {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        (_('Don'), {
            'fields': ('amount', 'currency', 'project', 'project_need', 'message')
        }),
        (_('Paiement'), {
            'fields': ('payment_method', 'status', 'stripe_payment_intent_id', 
                      'stripe_session_id', 'fapshi_transaction_id')
        }),
        (_('Suivi'), {
            'fields': ('receipt_sent', 'thank_you_sent', 'created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def reference_short(self, obj):
        return str(obj.reference)[:8]
    reference_short.short_description = _("Réf.")
    
    def donor_display(self, obj):
        return obj.display_name
    donor_display.short_description = _("Donateur")
    
    def project_display(self, obj):
        return obj.project.title if obj.project else _("Général")
    project_display.short_description = _("Projet")
    
    def status_badge(self, obj):
        colors = {
            'pending': '#F59E0B',
            'processing': '#3B82F6',
            'completed': '#10B981',
            'failed': '#EF4444',
            'refunded': '#8B5CF6',
            'cancelled': '#6B7280',
        }
        color = colors.get(obj.status, '#6B7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = _("Statut")
    
    actions = ['mark_completed', 'send_receipt', 'send_thank_you']
    
    @admin.action(description=_("Marquer comme complété"))
    def mark_completed(self, request, queryset):
        for donation in queryset.filter(status='pending'):
            donation.mark_completed()
        self.message_user(request, _("Les dons sélectionnés ont été marqués comme complétés."))
    
    @admin.action(description=_("Envoyer le reçu"))
    def send_receipt(self, request, queryset):
        # TODO: Implement receipt sending
        self.message_user(request, _("Fonctionnalité à implémenter"))
    
    @admin.action(description=_("Envoyer le remerciement"))
    def send_thank_you(self, request, queryset):
        # TODO: Implement thank you email
        self.message_user(request, _("Fonctionnalité à implémenter"))


@admin.register(MaterialContribution)
class MaterialContributionAdmin(admin.ModelAdmin):
    list_display = ['reference_short', 'contributor_name', 'project_need', 'quantity', 
                    'status', 'delivery_date']
    list_filter = ['status', 'created_at']
    search_fields = ['contributor_name', 'contributor_email', 'project_need__title']
    date_hierarchy = 'created_at'
    readonly_fields = ['reference', 'created_at', 'updated_at']
    
    def reference_short(self, obj):
        return str(obj.reference)[:8]
    reference_short.short_description = _("Réf.")
    
    actions = ['mark_delivered']
    
    @admin.action(description=_("Marquer comme livré"))
    def mark_delivered(self, request, queryset):
        for contribution in queryset.filter(status='confirmed'):
            contribution.mark_delivered()
        self.message_user(request, _("Les contributions sélectionnées ont été marquées comme livrées."))


@admin.register(DonationImpact)
class DonationImpactAdmin(admin.ModelAdmin):
    list_display = ['amount', 'currency', 'description_short', 'project_category', 'order']
    list_editable = ['order']
    list_filter = ['currency', 'project_category']
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = _("Description")
