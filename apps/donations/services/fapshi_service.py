"""
Fapshi Payment Service
Handles Fapshi mobile money payments for African users.
Fapshi supports MTN Mobile Money, Orange Money, and other local payment methods.
"""

import requests
import hmac
import hashlib
import json
from django.conf import settings
from decimal import Decimal
from datetime import datetime


class FapshiPaymentService:
    """Service class for Fapshi payment operations"""
    
    BASE_URL = "https://live.fapshi.com"  # Use sandbox.fapshi.com for testing
    
    def __init__(self):
        self.api_key = settings.FAPSHI_API_KEY
        self.api_secret = settings.FAPSHI_API_SECRET
    
    def _get_headers(self):
        """Get headers for Fapshi API requests"""
        return {
            'apiuser': self.api_key,
            'apikey': self.api_secret,
            'Content-Type': 'application/json',
        }
    
    def initiate_payment(
        self,
        amount: Decimal,
        donor_email: str,
        donor_phone: str,
        donor_name: str = "",
        project_id: int = None,
        project_need_id: int = None,
        message: str = "",
        redirect_url: str = None,
    ) -> dict:
        """
        Initiate a Fapshi payment.
        
        Args:
            amount: Amount in XAF (CFA Francs)
            donor_email: Donor's email
            donor_phone: Donor's phone number (required for mobile money)
            donor_name: Donor's name
            project_id: Optional project ID
            project_need_id: Optional project need ID
            message: Optional donation message
            redirect_url: URL to redirect after payment
            
        Returns:
            dict with transaction details
        """
        # Fapshi uses XAF (CFA Francs)
        amount_xaf = int(amount)
        
        # External ID for tracking
        external_id = f"FDTM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{donor_phone[-4:]}"
        
        payload = {
            'amount': amount_xaf,
            'email': donor_email,
            'phone': donor_phone,
            'externalId': external_id,
            'message': f"Don FDTM - {donor_name}" if donor_name else "Don à la Fondation FDTM",
            'redirectUrl': redirect_url or settings.SITE_URL + '/dons/succes/',
        }
        
        # Add metadata
        if project_id:
            payload['userId'] = str(project_id)  # Using userId field for project tracking
        
        try:
            response = requests.post(
                f"{self.BASE_URL}/initiate-pay",
                headers=self._get_headers(),
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'transaction_id': data.get('transId'),
                    'external_id': external_id,
                    'payment_link': data.get('link'),
                    'status': data.get('status'),
                }
            else:
                return {
                    'success': False,
                    'error': response.text,
                    'status_code': response.status_code,
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    def check_payment_status(self, transaction_id: str) -> dict:
        """
        Check the status of a Fapshi payment.
        
        Args:
            transaction_id: Fapshi transaction ID
            
        Returns:
            dict with payment status
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/payment-status/{transaction_id}",
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'status': data.get('status'),
                    'amount': data.get('amount'),
                    'transaction_id': data.get('transId'),
                    'medium': data.get('medium'),  # MTN, Orange, etc.
                    'payer_name': data.get('name'),
                    'payer_phone': data.get('phone'),
                }
            else:
                return {
                    'success': False,
                    'error': response.text,
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
            }
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """
        Verify Fapshi webhook signature.
        
        Args:
            payload: Raw webhook payload
            signature: Signature from webhook header
            
        Returns:
            bool indicating if signature is valid
        """
        expected_signature = hmac.new(
            self.api_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)


def process_fapshi_webhook(payload: dict):
    """
    Process Fapshi webhook notifications.
    
    Args:
        payload: Webhook payload from Fapshi
        
    Returns:
        Processed donation or None
    """
    from apps.donations.models import Donation
    from apps.projects.models import Project
    
    transaction_id = payload.get('transId')
    status = payload.get('status')
    
    if not transaction_id:
        return None
    
    # Check if donation exists
    try:
        donation = Donation.objects.get(fapshi_transaction_id=transaction_id)
    except Donation.DoesNotExist:
        # Create new donation from webhook data
        project = None
        project_id = payload.get('userId')  # We stored project_id in userId field
        
        if project_id:
            try:
                project = Project.objects.get(pk=int(project_id))
            except (Project.DoesNotExist, ValueError):
                pass
        
        donation = Donation.objects.create(
            donor_name=payload.get('name', 'Anonymous'),
            donor_email=payload.get('email', ''),
            donor_phone=payload.get('phone', ''),
            amount=Decimal(str(payload.get('amount', 0))),
            currency='XAF',
            project=project,
            payment_method='fapshi',
            fapshi_transaction_id=transaction_id,
            status='pending',
        )
    
    # Update status based on webhook
    if status == 'SUCCESSFUL':
        donation.mark_completed()
    elif status == 'FAILED':
        donation.status = 'failed'
        donation.save()
    elif status == 'EXPIRED':
        donation.status = 'cancelled'
        donation.save()
    
    return donation
