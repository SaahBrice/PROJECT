"""
Core Admin Configuration
Site settings, team, testimonials, partners, and contact messages.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    SiteSettings, TeamMember, Testimonial, Partner, 
    ImpactStat, FAQ, ContactMessage, Newsletter
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Singleton admin for site settings"""
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('site_name', 'tagline')
        }),
        (_('Contenu'), {
            'fields': ('about_text', 'mission_text', 'vision_text'),
            'classes': ('collapse',)
        }),
        (_('Contact'), {
            'fields': ('contact_email', 'contact_phone', 'address')
        }),
        (_('Réseaux sociaux'), {
            'fields': ('social_links',),
            'classes': ('collapse',)
        }),
        (_('Pied de page'), {
            'fields': ('footer_text',),
            'classes': ('collapse',)
        }),
        (_('SEO & Analytics'), {
            'fields': ('default_meta_description', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'role', 'photo_preview', 'is_active', 
                    'show_on_homepage', 'order']
    list_filter = ['role', 'is_active', 'show_on_homepage']
    list_editable = ['is_active', 'show_on_homepage', 'order']
    search_fields = ['name', 'title', 'bio']
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">',
                obj.photo.url
            )
        return "-"
    photo_preview.short_description = _("Photo")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'project', 'quote_preview', 'is_featured', 'is_active']
    list_filter = ['type', 'is_featured', 'is_active', 'project']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['name', 'quote']
    
    def quote_preview(self, obj):
        return obj.quote[:80] + '...' if len(obj.quote) > 80 else obj.quote
    quote_preview.short_description = _("Témoignage")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'logo_preview', 'is_active', 'order']
    list_filter = ['type', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['name', 'description']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height: 30px; max-width: 80px;">',
                obj.logo.url
            )
        return "-"
    logo_preview.short_description = _("Logo")


@admin.register(ImpactStat)
class ImpactStatAdmin(admin.ModelAdmin):
    list_display = ['title', 'value', 'suffix', 'is_active', 'order']
    list_editable = ['is_active', 'order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'is_active', 'order']
    list_filter = ['category', 'is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['question', 'answer']
    
    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = _("Question")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'is_replied', 'created_at']
    list_filter = ['is_read', 'is_replied', 'created_at']
    list_editable = ['is_read', 'is_replied']
    search_fields = ['name', 'email', 'subject', 'message']
    date_hierarchy = 'created_at'
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'ip_address', 'created_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'language', 'is_active', 'subscribed_at']
    list_filter = ['is_active', 'language', 'subscribed_at']
    list_editable = ['is_active']
    search_fields = ['email', 'name']
    date_hierarchy = 'subscribed_at'
    
    actions = ['export_emails']
    
    @admin.action(description=_("Exporter les emails"))
    def export_emails(self, request, queryset):
        # TODO: Implement email export
        self.message_user(request, _("Fonctionnalité à implémenter"))


# Customize admin site
admin.site.site_header = "FDTM Administration"
admin.site.site_title = "FDTM Admin"
admin.site.index_title = "Tableau de bord"
