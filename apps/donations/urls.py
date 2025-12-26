"""Donations App URLs"""

from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('', views.donate, name='donate'),
    path('projet/<slug:project_slug>/', views.donate_to_project, name='donate_to_project'),
    path('succes/', views.donation_success, name='success'),
    path('annule/', views.donation_cancelled, name='cancelled'),
    path('contribution-materielle/', views.material_contribution, name='material_contribution'),
    
    # Webhooks
    path('webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),
    path('webhook/fapshi/', views.fapshi_webhook, name='fapshi_webhook'),
]
