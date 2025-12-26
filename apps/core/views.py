"""
Core App Views
Homepage, about, contact, and legal pages.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import SiteSettings, TeamMember, Testimonial, Partner, ImpactStat, FAQ, ContactMessage, Newsletter, Event
from apps.projects.models import Project
from apps.articles.models import Article


def home(request):
    """Homepage with featured content"""
    context = {
        'featured_projects': Project.objects.filter(
            status='active', 
            is_featured=True
        ).select_related('category')[:3],
        'recent_articles': Article.objects.filter(
            status='published'
        ).select_related('category')[:3],
        'testimonials': Testimonial.objects.filter(
            is_active=True, 
            is_featured=True
        )[:3],
        'impact_stats': ImpactStat.objects.filter(is_active=True),
        'partners': Partner.objects.filter(is_active=True)[:6],
        'upcoming_events': Event.objects.filter(
            is_published=True,
            event_date__gt=timezone.now()
        )[:3],
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page with team and values"""
    context = {
        'settings': SiteSettings.get_settings(),
        'team_members': TeamMember.objects.filter(is_active=True),
        'testimonials': Testimonial.objects.filter(is_active=True)[:6],
        'partners': Partner.objects.filter(is_active=True),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        
        if name and email and subject and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, _("Votre message a été envoyé avec succès. Nous vous répondrons bientôt."))
            return redirect('core:contact')
        else:
            messages.error(request, _("Veuillez remplir tous les champs obligatoires."))
    
    context = {
        'settings': SiteSettings.get_settings(),
        'faqs': FAQ.objects.filter(is_active=True),
    }
    return render(request, 'core/contact.html', context)


def privacy(request):
    """Privacy policy page"""
    return render(request, 'core/privacy.html')


def terms(request):
    """Terms of service / legal mentions page"""
    return render(request, 'core/terms.html')


def newsletter_subscribe(request):
    """Newsletter subscription handler"""
    if request.method == 'POST':
        email = request.POST.get('email', '')
        name = request.POST.get('name', '')
        
        if email:
            newsletter, created = Newsletter.objects.get_or_create(
                email=email,
                defaults={'name': name, 'language': request.LANGUAGE_CODE}
            )
            if created:
                messages.success(request, _("Merci pour votre inscription à notre newsletter !"))
            else:
                messages.info(request, _("Vous êtes déjà inscrit à notre newsletter."))
        
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))


def events_list(request):
    """Events page with animated timeline"""
    upcoming_events = Event.objects.filter(
        is_published=True,
        event_date__gt=timezone.now()
    ).order_by('event_date')
    
    past_events = Event.objects.filter(
        is_published=True,
        event_date__lte=timezone.now()
    ).order_by('-event_date')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'core/events.html', context)

