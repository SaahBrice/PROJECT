"""
Projects Admin Configuration
Beautiful admin interface for managing projects, needs, and updates.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import ProjectCategory, Project, ProjectNeed, ProjectUpdate


class ProjectNeedInline(admin.TabularInline):
    """Inline editor for project needs"""
    model = ProjectNeed
    extra = 1
    fields = ['need_type', 'title', 'target_amount', 'current_amount', 
              'item_name', 'quantity_needed', 'quantity_received', 'priority', 'is_fulfilled']


class ProjectUpdateInline(admin.StackedInline):
    """Inline editor for project updates"""
    model = ProjectUpdate
    extra = 0
    fields = ['title', 'content', 'image', 'is_milestone']


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color_preview', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; border-radius: 4px; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_preview.short_description = _("Couleur")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'progress_bar', 'is_featured', 'is_urgent', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'is_urgent']
    list_editable = ['is_featured', 'is_urgent']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    inlines = [ProjectNeedInline, ProjectUpdateInline]
    
    fieldsets = (
        (_('Informations de base'), {
            'fields': ('title', 'slug', 'category', 'short_description', 'description')
        }),
        (_('Impact'), {
            'fields': ('impact_description',)
        }),
        (_('Médias'), {
            'fields': ('featured_image', 'video_url'),
            'classes': ('collapse',)
        }),
        (_('Localisation'), {
            'fields': ('location', 'location_coordinates'),
            'classes': ('collapse',)
        }),
        (_('Financement'), {
            'fields': ('goal_amount', 'current_amount', 'currency'),
        }),
        (_('Statut'), {
            'fields': ('status', 'is_featured', 'is_urgent', 'start_date', 'end_date'),
        }),
    )
    
    def progress_bar(self, obj):
        percentage = obj.progress_percentage
        color = '#10B981' if percentage >= 100 else '#C75B2A'
        return format_html(
            '''<div style="width: 100px; background: #E5E7EB; border-radius: 10px; overflow: hidden;">
                <div style="width: {}%; background: {}; height: 10px;"></div>
            </div>
            <small style="color: #6B7280;">{}%</small>''',
            percentage, color, round(percentage, 1)
        )
    progress_bar.short_description = _("Progression")


@admin.register(ProjectNeed)
class ProjectNeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'need_type', 'progress_display', 'priority', 'is_fulfilled']
    list_filter = ['need_type', 'is_fulfilled', 'project']
    list_editable = ['priority', 'is_fulfilled']
    search_fields = ['title', 'project__title']
    
    def progress_display(self, obj):
        percentage = obj.progress_percentage
        if obj.need_type == 'financial':
            return f"{obj.current_amount} / {obj.target_amount} ({percentage:.0f}%)"
        else:
            return f"{obj.quantity_received} / {obj.quantity_needed} ({percentage:.0f}%)"
    progress_display.short_description = _("Progression")


@admin.register(ProjectUpdate)
class ProjectUpdateAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'is_milestone', 'created_at']
    list_filter = ['is_milestone', 'project', 'created_at']
    search_fields = ['title', 'content', 'project__title']
    date_hierarchy = 'created_at'
