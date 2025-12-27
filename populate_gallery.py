"""
Script to populate gallery with dummy images
Run with: python manage.py shell < populate_gallery.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fdtm.settings')
django.setup()

from apps.core.models import GalleryImage
from apps.projects.models import Project

# Get some projects to associate with images
projects = list(Project.objects.all()[:3])

# Dummy gallery images - NGO/humanitarian themed from Unsplash
gallery_data = [
    {
        "title": "Distribution alimentaire",
        "caption": "Distribution de vivres aux familles dans le besoin",
        "image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800",
        "location": "Douala, Cameroun",
        "is_featured": True,
    },
    {
        "title": "Cours de soutien scolaire",
        "caption": "Les enfants bénéficient de cours gratuits",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800",
        "location": "Yaoundé, Cameroun",
        "is_featured": True,
    },
    {
        "title": "Construction d'un puits",
        "caption": "Accès à l'eau potable pour le village",
        "image_url": "https://images.unsplash.com/photo-1594708767771-a7502f525aa0?w=800",
        "location": "Bafoussam, Cameroun",
        "is_featured": True,
    },
    {
        "title": "Visite médicale",
        "caption": "Campagne de santé gratuite pour les enfants",
        "image_url": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800",
        "location": "Douala, Cameroun",
    },
    {
        "title": "Réunion communautaire",
        "caption": "Échange avec les leaders locaux",
        "image_url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800",
        "location": "Bamenda, Cameroun",
    },
    {
        "title": "Formation agricole",
        "caption": "Enseigner les techniques agricoles modernes",
        "image_url": "https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=800",
        "location": "Maroua, Cameroun",
    },
    {
        "title": "Sourires d'enfants",
        "caption": "La joie des enfants lors de nos activités",
        "image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800",
        "location": "Garoua, Cameroun",
    },
    {
        "title": "Distribution de fournitures",
        "caption": "Cahiers et stylos pour la rentrée",
        "image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
        "location": "Douala, Cameroun",
    },
    {
        "title": "Atelier couture",
        "caption": "Formation professionnelle pour les femmes",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
        "location": "Yaoundé, Cameroun",
    },
    {
        "title": "Plantation d'arbres",
        "caption": "Action environnementale avec les jeunes",
        "image_url": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=800",
        "location": "Kribi, Cameroun",
    },
    {
        "title": "Fête communautaire",
        "caption": "Célébration avec nos bénéficiaires",
        "image_url": "https://images.unsplash.com/photo-1511632765486-a01980e01a18?w=800",
        "location": "Bafoussam, Cameroun",
    },
    {
        "title": "Aide aux personnes âgées",
        "caption": "Soutien aux aînés isolés",
        "image_url": "https://images.unsplash.com/photo-1516307365426-bea591f05011?w=800",
        "location": "Douala, Cameroun",
    },
    {
        "title": "Construction école",
        "caption": "Nouvelle salle de classe en cours",
        "image_url": "https://images.unsplash.com/photo-1541829070764-84a7d30dd3f3?w=800",
        "location": "Ngaoundéré, Cameroun",
    },
    {
        "title": "Camp de vacances",
        "caption": "Activités récréatives pour les orphelins",
        "image_url": "https://images.unsplash.com/photo-1472162072942-cd5147eb3902?w=800",
        "location": "Limbe, Cameroun",
    },
    {
        "title": "Sensibilisation santé",
        "caption": "Information sur l'hygiène et la prévention",
        "image_url": "https://images.unsplash.com/photo-1584515933487-779824d29309?w=800",
        "location": "Douala, Cameroun",
    },
    {
        "title": "Équipe de bénévoles",
        "caption": "Nos bénévoles sur le terrain",
        "image_url": "https://images.unsplash.com/photo-1559027615-cd4628902d4a?w=800",
        "location": "Yaoundé, Cameroun",
    },
    {
        "title": "Microcrédit femmes",
        "caption": "Remise de fonds pour les petits commerces",
        "image_url": "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=800",
        "location": "Bafoussam, Cameroun",
    },
    {
        "title": "Bibliothèque mobile",
        "caption": "Livres pour les enfants des villages",
        "image_url": "https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800",
        "location": "Bertoua, Cameroun",
    },
    {
        "title": "Sport pour tous",
        "caption": "Tournoi de football solidaire",
        "image_url": "https://images.unsplash.com/photo-1431324155629-1a6deb1dec8d?w=800",
        "location": "Douala, Cameroun",
    },
    {
        "title": "Remise de diplômes",
        "caption": "Fin de formation des apprenants",
        "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800",
        "location": "Yaoundé, Cameroun",
    },
]

# Clear existing gallery images
print("Clearing existing gallery images...")
GalleryImage.objects.all().delete()

# Create new gallery images
print("Creating 20 gallery images...")
for i, data in enumerate(gallery_data):
    # Associate some images with projects
    project = None
    if projects and i % 3 == 0:
        project = projects[i % len(projects)]
    
    GalleryImage.objects.create(
        title=data.get("title", ""),
        caption=data.get("caption", ""),
        image_url=data.get("image_url", ""),
        location=data.get("location", ""),
        is_featured=data.get("is_featured", False),
        is_published=True,
        project=project,
    )
    print(f"  Created: {data['title']}")

print(f"\nDone! Created {GalleryImage.objects.count()} gallery images.")
