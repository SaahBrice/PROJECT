"""
Stripe Payment Service
Handles Stripe checkout sessions and payment processing.
"""

import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal


# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:
    """Service class for Stripe payment operations"""
    
    @staticmethod
    def create_checkout_session(
        amount: Decimal,
        currency: str,
        donor_email: str,
        project_id: int = None,
        project_need_id: int = None,
        donor_name: str = "",
        message: str = "",
        success_url: str = None,
        cancel_url: str = None,
        metadata: dict = None
    ) -> dict:
        """
        Create a Stripe Checkout Session for a donation.
        
        Args:
            amount: Donation amount in major currency units (e.g., euros)
            currency: 3-letter currency code (EUR, USD, etc.)
            donor_email: Donor's email address
            project_id: Optional project ID for project-specific donations
            project_need_id: Optional project need ID
            donor_name: Donor's name
            message: Optional donation message
            success_url: URL to redirect after successful payment
            cancel_url: URL to redirect after cancelled payment
            metadata: Additional metadata to store
            
        Returns:
            dict with session_id and checkout_url
        """
        # Convert amount to cents
        amount_cents = int(amount * 100)
        
        # Build metadata
        session_metadata = {
            'donor_name': donor_name,
            'donor_email': donor_email,
            'message': message[:500] if message else '',
        }
        
        if project_id:
            session_metadata['project_id'] = str(project_id)
        if project_need_id:
            session_metadata['project_need_id'] = str(project_need_id)
        if metadata:
            session_metadata.update(metadata)
        
        # Create checkout session
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency.lower(),
                        'unit_amount': amount_cents,
                        'product_data': {
                            'name': 'Don à la Fondation FDTM',
                            'description': f'Don de {amount} {currency}' + 
                                          (f' pour le projet' if project_id else ' - Fonds général'),
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                customer_email=donor_email,
                success_url=success_url or settings.SITE_URL + reverse('donations:success') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url or settings.SITE_URL + reverse('donations:cancelled'),
                metadata=session_metadata,
            )
            
            return {
                'success': True,
                'session_id': session.id,
                'checkout_url': session.url,
            }
            
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    @staticmethod
    def retrieve_session(session_id: str) -> dict:
        """Retrieve a checkout session by ID"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return {
                'success': True,
                'session': session,
                'payment_status': session.payment_status,
                'customer_email': session.customer_email,
                'amount_total': session.amount_total / 100,
                'currency': session.currency.upper(),
                'metadata': session.metadata,
            }
        except stripe.error.StripeError as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    @staticmethod
    def construct_webhook_event(payload: bytes, sig_header: str) -> dict:
        """Construct and verify a webhook event"""
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
            return {
                'success': True,
                'event': event,
            }
        except ValueError:
            return {
                'success': False,
                'error': 'Invalid payload',
            }
        except stripe.error.SignatureVerificationError:
            return {
                'success': False,
                'error': 'Invalid signature',
            }


def process_stripe_webhook(event):
    """
    Process Stripe webhook events.
    
    Args:
        event: Stripe event object
        
    Returns:
        Processed donation or None
    """
    from apps.donations.models import Donation
    from apps.projects.models import Project, ProjectNeed
    
    event_type = event['type']
    data = event['data']['object']
    
    if event_type == 'checkout.session.completed':
        session_id = data['id']
        metadata = data.get('metadata', {})
        
        # Check if donation already exists
        try:
            donation = Donation.objects.get(stripe_session_id=session_id)
        except Donation.DoesNotExist:
            # Create new donation record
            project = None
            project_need = None
            
            if metadata.get('project_id'):
                try:
                    project = Project.objects.get(pk=int(metadata['project_id']))
                except (Project.DoesNotExist, ValueError):
                    pass
            
            if metadata.get('project_need_id'):
                try:
                    project_need = ProjectNeed.objects.get(pk=int(metadata['project_need_id']))
                except (ProjectNeed.DoesNotExist, ValueError):
                    pass
            
            donation = Donation.objects.create(
                donor_name=metadata.get('donor_name', 'Anonymous'),
                donor_email=data.get('customer_email', ''),
                amount=Decimal(data['amount_total']) / 100,
                currency=data['currency'].upper(),
                project=project,
                project_need=project_need,
                payment_method='stripe',
                stripe_session_id=session_id,
                stripe_payment_intent_id=data.get('payment_intent', ''),
                message=metadata.get('message', ''),
            )
        
        # Mark as completed
        donation.mark_completed()
        return donation
    
    elif event_type == 'payment_intent.payment_failed':
        payment_intent_id = data['id']
        try:
            donation = Donation.objects.get(stripe_payment_intent_id=payment_intent_id)
            donation.status = 'failed'
            donation.save()
            return donation
        except Donation.DoesNotExist:
            pass
    
    return None
