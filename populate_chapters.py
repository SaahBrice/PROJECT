"""
Script to populate homepage chapters with realistic, solution-focused stories
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

# Realistic, solution-focused stories - FDTM creates lasting solutions, not just handouts
chapters_data = [
    {
        "chapter_number": 1,
        "title": "« Maintenant, c'est moi qui aide les autres mamans. »",
        "subtitle": "Jeanne, 45 ans, relais communautaire à Bafoussam",
        "content": """Jeanne a perdu son premier enfant à cause d'une fièvre mal traitée. Personne dans son village ne savait reconnaître les signes de danger.

Avec le soutien de FDTM, elle a suivi une formation de relais communautaire. Aujourd'hui, elle sensibilise les familles de son quartier aux premiers gestes de santé. Elle a déjà orienté 12 enfants vers le dispensaire à temps.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800",
        "dark_background": False,
        "accent_color": "#0066FF",
        "stats": [{"value": "45", "label": "relais formés"}],
        "order": 1,
    },
    {
        "chapter_number": 2,
        "title": "« L'école, c'est mon investissement pour demain. »",
        "subtitle": "Arouna, 17 ans, boursier en classe de Terminale",
        "content": """Le père d'Arouna cultive le maïs. Les bonnes années, ça suffit. Les mauvaises, il faut choisir entre manger et payer l'école.

Avec une bourse FDTM, Arouna ne dépend plus des récoltes. Il prépare son baccalauréat et veut devenir comptable pour aider les agriculteurs de son village à mieux gérer leurs revenus.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800",
        "dark_background": False,
        "accent_color": "#0066FF",
        "stats": [{"value": "38", "label": "boursiers cette année"}],
        "order": 2,
    },
    {
        "chapter_number": 3,
        "title": "« Mon commerce nourrit ma famille et fait vivre deux autres personnes. »",
        "subtitle": "Marie-Claire, 34 ans, commerçante à Douala",
        "content": """Marie-Claire a perdu son mari il y a 3 ans. Avec 4 enfants à charge, elle vendait des beignets au bord de la route.

FDTM lui a fourni un fonds de démarrage et une formation en gestion. Aujourd'hui, elle a un stand au marché central, emploie deux vendeuses, et ses enfants sont tous scolarisés.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1593113598332-cd288d649433?w=800",
        "dark_background": False,
        "accent_color": "#00C49A",
        "stats": [{"value": "28", "label": "micro-entreprises créées"}],
        "cta_text": "Soutenir un projet",
        "cta_url": "donations:donate",
        "order": 3,
    },
    {
        "chapter_number": 4,
        "title": "« Mes enfants ont les mêmes chances que les autres. »",
        "subtitle": "Emmanuel, 42 ans, père de 3 enfants à Yaoundé",
        "content": """Emmanuel est gardien de nuit. Son salaire couvre le loyer et la nourriture. Pour les frais scolaires, c'était toujours l'angoisse de septembre.

Grâce au programme de parrainage FDTM, ses trois enfants reçoivent chaque année leur kit scolaire complet. Emmanuel peut maintenant épargner pour leur avenir au lieu de s'endetter chaque rentrée.""",
        "chapter_type": "story",
        "background_image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=800",
        "dark_background": False,
        "accent_color": "#FF6B35",
        "stats": [{"value": "85", "label": "familles parrainées"}],
        "order": 4,
    },
]

print("Creating homepage chapters...")
for data in chapters_data:
    HomeChapter.objects.create(**data, is_published=True)
    print(f"  Created: Chapitre {data['chapter_number']} - {data['title'][:40]}...")

print(f"\nDone! Created {HomeChapter.objects.count()} chapters.")
