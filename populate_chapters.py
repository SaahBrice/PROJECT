"""
Script to populate homepage chapters with realistic dummy data
Run with: python populate_chapters.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fdtm.settings')
django.setup()

from apps.core.models import HomeChapter

# Clear existing chapters
print("Clearing existing chapters...")
HomeChapter.objects.all().delete()

# Create realistic chapters about family donations
chapters_data = [
    {
        "chapter_number": 3,
        "title": "Notre action au quotidien",
        "subtitle": "Des dons qui changent des vies",
        "content": """Depuis 2018, nous agissons directement auprès des familles vulnérables au Cameroun. 
Notre approche est simple : apporter une aide concrète, humaine et personnalisée.

Chaque don que nous recevons est redistribué intégralement aux bénéficiaires sous forme d'aide financière, de vivres, de vêtements ou de matériel scolaire.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=1600",
        "dark_background": True,
        "accent_color": "#0066FF",
        "cta_text": "Voir nos projets",
        "cta_url": "projects:list",
        "order": 1,
    },
    {
        "chapter_number": 4,
        "title": "L'impact de votre générosité",
        "subtitle": "Des chiffres qui parlent",
        "content": "Grâce à vous, nous avons pu soutenir des centaines de familles camerounaises.",
        "chapter_type": "impact",
        "background_image_url": "https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=1600",
        "dark_background": True,
        "accent_color": "#00C49A",
        "stats": [
            {"value": "520+", "label": "Familles soutenues"},
            {"value": "850K", "label": "FCFA distribués"},
            {"value": "12", "label": "Villages touchés"},
            {"value": "150+", "label": "Kits scolaires"},
            {"value": "200+", "label": "Paniers alimentaires"},
            {"value": "7", "label": "Années d'action"},
        ],
        "cta_text": "Faire un don",
        "cta_url": "donations:donate",
        "order": 2,
    },
    {
        "chapter_number": 5,
        "title": "Chaque geste compte",
        "subtitle": "Témoignage d'une famille accompagnée",
        "content": """\"Quand la Fondation FDTM est venue chez nous avec des vivres et de l'argent pour payer les frais de scolarité de mes enfants, j'ai compris que nous n'étions pas seuls. Ce soutien a changé notre vie.\"

— Maman Marie, Douala""",
        "chapter_type": "testimonial",
        "background_image_url": "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=1600",
        "dark_background": True,
        "accent_color": "#FF6B35",
        "cta_text": "Lire d'autres témoignages",
        "cta_url": "core:about",
        "order": 3,
    },
]

print("Creating homepage chapters...")
for data in chapters_data:
    HomeChapter.objects.create(**data, is_published=True)
    print(f"  Created: Chapitre {data['chapter_number']} - {data['title']}")

print(f"\nDone! Created {HomeChapter.objects.count()} chapters.")
