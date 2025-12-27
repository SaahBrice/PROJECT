"""
Donations App Signals
Handles automatic project amount updates when donations are completed.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(pre_save, sender='donations.Donation')
def track_donation_status_change(sender, instance, **kwargs):
    """
    Track if the donation status is changing to 'completed' so we can update project amounts.
    We use pre_save to capture the old status before it changes.
    """
    if instance.pk:
        # Existing donation - check if status is changing
        try:
            from .models import Donation
            old_donation = Donation.objects.get(pk=instance.pk)
            instance._old_status = old_donation.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        # New donation
        instance._old_status = None


@receiver(post_save, sender='donations.Donation')
def update_project_on_donation_complete(sender, instance, created, **kwargs):
    """
    Update project current_amount and project_need current_amount when a donation is completed.
    Handles both:
    - New donations created with status='completed'
    - Existing donations that had their status changed to 'completed'
    """
    from decimal import Decimal
    
    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status
    
    # Check if donation is newly completed
    is_newly_completed = (
        new_status == 'completed' and 
        (created or old_status != 'completed')
    )
    
    if is_newly_completed:
        # Set completed_at if not already set
        if not instance.completed_at:
            instance.completed_at = timezone.now()
            # Use update to avoid triggering signals again
            sender.objects.filter(pk=instance.pk).update(completed_at=instance.completed_at)
        
        # Update project current_amount
        if instance.project:
            from apps.projects.models import Project
            project = instance.project
            project.current_amount = (project.current_amount or Decimal('0')) + instance.amount
            project.save(update_fields=['current_amount'])
            
            # Update specific project need if applicable
            if instance.project_need:
                need = instance.project_need
                need.current_amount = (need.current_amount or Decimal('0')) + instance.amount
                need.save(update_fields=['current_amount'])
    
    # Handle refunds - subtract from project amounts
    is_newly_refunded = (
        new_status == 'refunded' and
        old_status == 'completed'
    )
    
    if is_newly_refunded:
        if instance.project:
            from apps.projects.models import Project
            project = instance.project
            project.current_amount = max((project.current_amount or Decimal('0')) - instance.amount, Decimal('0'))
            project.save(update_fields=['current_amount'])
            
            if instance.project_need:
                need = instance.project_need
                need.current_amount = max((need.current_amount or Decimal('0')) - instance.amount, Decimal('0'))
                need.save(update_fields=['current_amount'])


@receiver(post_save, sender='donations.MaterialContribution')
def update_need_on_material_delivered(sender, instance, created, **kwargs):
    """
    Update project need quantity_received when a material contribution is delivered.
    """
    old_status = getattr(instance, '_old_status', None)
    new_status = instance.status
    
    # Check if contribution is newly delivered
    is_newly_delivered = (
        new_status == 'delivered' and
        (created or old_status != 'delivered')
    )
    
    if is_newly_delivered and instance.project_need:
        need = instance.project_need
        need.quantity_received = (need.quantity_received or 0) + instance.quantity
        need.save(update_fields=['quantity_received'])


@receiver(pre_save, sender='donations.MaterialContribution')
def track_material_status_change(sender, instance, **kwargs):
    """Track material contribution status changes."""
    if instance.pk:
        try:
            from .models import MaterialContribution
            old = MaterialContribution.objects.get(pk=instance.pk)
            instance._old_status = old.status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None
