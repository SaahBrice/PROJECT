"""
Core Admin Configuration
Site settings, team, testimonials, partners, and contact messages.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import (
    SiteSettings, TeamMember, Testimonial, Partner, 
    ImpactStat, FAQ, ContactMessage, Newsletter, Event, GalleryImage
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


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_date', 'location', 'is_featured', 'is_published', 'image_preview']
    list_filter = ['is_featured', 'is_published', 'event_date', 'project']
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'event_date'
    autocomplete_fields = ['project']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'short_description', 'description')
        }),
        (_('Date et lieu'), {
            'fields': ('event_date', 'end_date', 'location', 'address')
        }),
        (_('Image'), {
            'fields': ('image', 'image_url')
        }),
        (_('Association'), {
            'fields': ('project',)
        }),
        (_('Options'), {
            'fields': ('is_featured', 'is_published')
        }),
    )
    
    def image_preview(self, obj):
        url = obj.image.url if obj.image else obj.image_url
        if url:
            return format_html('<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;">', url)
        return "-"
    image_preview.short_description = _("Image")


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    """Admin for gallery images with bulk upload support"""
    list_display = ['image_preview', 'title', 'project', 'location', 'is_featured', 'is_published', 'created_at']
    list_filter = ['is_featured', 'is_published', 'project', 'created_at']
    list_editable = ['is_featured', 'is_published']
    search_fields = ['title', 'caption', 'location', 'photographer']
    autocomplete_fields = ['project']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('title', 'caption')
        }),
        (_('Image'), {
            'fields': ('image', 'image_url'),
            'description': _('Téléchargez une image ou fournissez une URL externe')
        }),
        (_('Projet associé'), {
            'fields': ('project',)
        }),
        (_('Métadonnées'), {
            'fields': ('location', 'date_taken', 'photographer'),
            'classes': ('collapse',)
        }),
        (_('Affichage'), {
            'fields': ('is_featured', 'is_published', 'order')
        }),
    )
    
    def image_preview(self, obj):
        url = obj.get_image_url
        if url:
            return format_html(
                '<img src="{}" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px;">',
                url
            )
        return "-"
    image_preview.short_description = _("Aperçu")
    
    # Allow bulk actions
    actions = ['make_featured', 'make_unfeatured', 'publish', 'unpublish']
    
    @admin.action(description=_("Mettre en avant"))
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    
    @admin.action(description=_("Retirer de la mise en avant"))
    def make_unfeatured(self, request, queryset):
        queryset.update(is_featured=False)
    
    @admin.action(description=_("Publier"))
    def publish(self, request, queryset):
        queryset.update(is_published=True)
    
    @admin.action(description=_("Dépublier"))
    def unpublish(self, request, queryset):
        queryset.update(is_published=False)


from .models import HomeChapter

@admin.register(HomeChapter)
class HomeChapterAdmin(admin.ModelAdmin):
    """Admin for homepage chapters with preview and ordering"""
    list_display = ['chapter_number', 'title', 'chapter_type', 'image_preview', 'is_published', 'order']
    list_filter = ['chapter_type', 'is_published', 'dark_background']
    list_editable = ['is_published', 'order']
    search_fields = ['title', 'subtitle', 'content']
    ordering = ['order', 'chapter_number']
    
    fieldsets = (
        (None, {
            'fields': ('chapter_number', 'title', 'subtitle', 'content')
        }),
        (_('Type et style'), {
            'fields': ('chapter_type', 'accent_color', 'dark_background')
        }),
        (_('Image de fond'), {
            'fields': ('background_image', 'background_image_url', 'gallery_image'),
            'description': _('Choisissez UNE option: upload, URL, ou image de la galerie')
        }),
        (_('Appel à l\'action'), {
            'fields': ('cta_text', 'cta_url'),
            'classes': ('collapse',)
        }),
        (_('Statistiques (pour chapitres Impact)'), {
            'fields': ('stats',),
            'classes': ('collapse',),
            'description': _('Format JSON: [{"value": "520+", "label": "Familles"}]')
        }),
        (_('Affichage'), {
            'fields': ('order', 'is_published')
        }),
    )
    
    def image_preview(self, obj):
        url = obj.get_background_url
        if url:
            return format_html(
                '<img src="{}" style="width: 80px; height: 50px; object-fit: cover; border-radius: 8px;">',
                url
            )
        return "-"
    image_preview.short_description = _("Aperçu")


# Customize admin site
admin.site.site_header = "FDTM Administration"
admin.site.site_title = "FDTM Admin"
admin.site.index_title = "Tableau de bord"


