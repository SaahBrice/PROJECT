"""
Donations App Views
Donation flow, payment processing, and webhooks.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Donation, MaterialContribution, DonationImpact
from apps.projects.models import Project, ProjectNeed


def donate(request):
    """General donation page"""
    from apps.core.models import FAQ
    
    # Get material needs for in-kind donation form
    material_needs = ProjectNeed.objects.filter(
        need_type='material',
        is_fulfilled=False
    ).select_related('project')
    
    context = {
        'projects': Project.objects.filter(status='active'),
        'impact_examples': DonationImpact.objects.all()[:6],
        'featured_impacts': DonationImpact.objects.filter(is_featured=True)[:3],
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'faqs': FAQ.objects.filter(is_active=True)[:10],
        'material_needs': material_needs,
    }
    return render(request, 'donations/donate.html', context)


def donate_to_project(request, project_slug):
    """Donation page for a specific project"""
    project = get_object_or_404(Project, slug=project_slug, status='active')
    
    context = {
        'project': project,
        'needs': project.needs.filter(is_fulfilled=False),
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'donations/donate_project.html', context)


def donation_success(request):
    """Donation success page"""
    return render(request, 'donations/success.html')


def donation_cancelled(request):
    """Donation cancelled page"""
    return render(request, 'donations/cancelled.html')


def material_contribution(request):
    """Material contribution form"""
    if request.method == 'POST':
        # Handle form submission
        project_need_id = request.POST.get('project_need')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity', 1)
        
        try:
            project_need = ProjectNeed.objects.get(pk=project_need_id)
            
            MaterialContribution.objects.create(
                project_need=project_need,
                contributor_name=name,
                contributor_email=email,
                contributor_phone=phone,
                description=description,
                quantity=int(quantity)
            )
            
            messages.success(request, _("Merci pour votre engagement ! Nous vous contacterons bientôt."))
            return redirect('donations:donate')
            
        except ProjectNeed.DoesNotExist:
            messages.error(request, _("Ce besoin n'existe plus."))
    
    # Get all material needs
    material_needs = ProjectNeed.objects.filter(
        need_type='material',
        is_fulfilled=False
    ).select_related('project')
    
    context = {
        'material_needs': material_needs,
    }
    return render(request, 'donations/material_contribution.html', context)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    import stripe
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Find and update the donation
        try:
            donation = Donation.objects.get(stripe_session_id=session['id'])
            donation.stripe_payment_intent_id = session.get('payment_intent', '')
            donation.mark_completed()
        except Donation.DoesNotExist:
            pass
    
    elif event['type'] == 'payment_intent.payment_failed':
        intent = event['data']['object']
        try:
            donation = Donation.objects.get(stripe_payment_intent_id=intent['id'])
            donation.status = 'failed'
            donation.save()
        except Donation.DoesNotExist:
            pass
    
    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def fapshi_webhook(request):
    """Handle Fapshi webhooks"""
    # TODO: Implement Fapshi webhook handling
    # Will be implemented when Fapshi integration is added
    return HttpResponse(status=200)
