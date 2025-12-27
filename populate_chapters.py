"""
Script to populate homepage chapters with narrative style content
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

# Create realistic chapters matching the existing beautiful narrative style
chapters_data = [
    {
        "chapter_number": 1,
        "title": "« Avant, je marchais 12 km pour voir un médecin. »",
        "subtitle": "Maman Rose, 67 ans, guérisseuse traditionnelle à Foto",
        "content": """Quand le centre de santé a ouvert ses portes, elle a pleuré. Pas de tristesse — de soulagement.

Aujourd'hui, elle travaille main dans la main avec les infirmières. Son savoir ancestral rencontre la médecine moderne. Ses petits-enfants sont vaccinés.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
        "dark_background": False,
        "accent_color": "#0066FF",
        "stats": [{"value": "3 200", "label": "consultations en 2024"}],
        "order": 1,
    },
    {
        "chapter_number": 2,
        "title": "« Je serai médecin. Comme ceux qui ont soigné ma mère. »",
        "subtitle": "Arouna M., boursier depuis 2022",
        "content": """Arouna, 16 ans. Son père est cultivateur. Sa mère a survécu à une complication pendant l'accouchement grâce au centre de santé. Depuis, il a une mission.

Grâce à une bourse FDTM, il est premier de sa classe au lycée de Dschang. Dans 7 ans, il rentrera au village. Avec une blouse blanche.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
        "dark_background": False,
        "accent_color": "#0066FF",
        "stats": [{"value": "127", "label": "boursiers cette année"}],
        "order": 2,
    },
    {
        "chapter_number": 3,
        "title": "« Mes enfants ont mangé à leur faim cette année. »",
        "subtitle": "Marie-Claire, mère de 4 enfants à Douala",
        "content": """Marie-Claire a perdu son mari en 2021. Avec 4 enfants à nourrir et pas de travail stable, chaque jour était un combat.

Grâce à l'aide alimentaire et au soutien financier de FDTM, elle a pu ouvrir un petit commerce de légumes. Aujourd'hui, elle emploie deux personnes.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800",
        "dark_background": False,
        "accent_color": "#00C49A",
        "stats": [{"value": "520+", "label": "familles soutenues"}],
        "cta_text": "Soutenir une famille",
        "cta_url": "donations:donate",
        "order": 3,
    },
    {
        "chapter_number": 4,
        "title": "« La rentrée scolaire n'est plus un cauchemar. »",
        "subtitle": "Jean-Pierre, père de 3 enfants",
        "content": """Chaque année, Jean-Pierre devait choisir : payer les frais scolaires ou acheter les fournitures. Jamais les deux.

Avec les kits scolaires distribués par FDTM — cahiers, stylos, uniformes — ses trois enfants sont équipés. Et lui peut garder son salaire pour la nourriture.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800",
        "dark_background": False,
        "accent_color": "#FF6B35",
        "stats": [{"value": "150+", "label": "kits scolaires distribués"}],
        "order": 4,
    },
]

print("Creating homepage chapters...")
for data in chapters_data:
    HomeChapter.objects.create(**data, is_published=True)
    print(f"  Created: Chapitre {data['chapter_number']} - {data['title'][:50]}...")

print(f"\nDone! Created {HomeChapter.objects.count()} chapters.")
