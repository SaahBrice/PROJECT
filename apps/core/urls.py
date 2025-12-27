"""Core App URLs"""

from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('confidentialite/', views.privacy, name='privacy'),
    path('mentions-legales/', views.terms, name='terms'),
    path('newsletter/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('evenements/', views.events_list, name='events'),
    path('galerie/', views.gallery, name='gallery'),
]



