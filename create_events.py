import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fdtm.settings.development')
django.setup()

from django.utils import timezone
from datetime import timedelta
from apps.core.models import Event

# Clear existing events
Event.objects.all().delete()

# Create events - both upcoming and past
events = [
    # UPCOMING EVENTS
    {
        'title': 'Festival Culturel Nkamsi 2025',
        'description': 'Le plus grand rassemblement culturel de la region Ouest. Trois jours de danses traditionnelles, musique, artisanat et gastronomie locale.',
        'short_description': 'Trois jours de celebration culturelle : danses, musique, artisanat et gastronomie.',
        'event_date': timezone.now() + timedelta(days=45, hours=10),
        'end_date': timezone.now() + timedelta(days=48),
        'location': 'Place du Marche, Dschang',
        'address': 'Place du Marche Central, Dschang, Region Ouest, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Journee Portes Ouvertes - Centre de Sante Foto',
        'description': 'Venez decouvrir notre centre de sante communautaire ! Consultations gratuites, depistage, vaccination.',
        'short_description': 'Consultations gratuites, depistage et vaccination. Decouvrez notre centre.',
        'event_date': timezone.now() + timedelta(days=15, hours=8),
        'location': 'Centre de Sante Foto',
        'address': 'Foto, a 8km de Dschang',
        'image_url': 'https://images.unsplash.com/photo-1584515933487-779824d29309?w=800',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Remise des Bourses Scolaires 2025',
        'description': 'Ceremonie officielle de remise des bourses aux 50 nouveaux eleves beneficiaires du programme FDTM.',
        'short_description': 'Ceremonie de remise des bourses aux 50 nouveaux eleves.',
        'event_date': timezone.now() + timedelta(days=30, hours=14),
        'location': 'Lycee de Dschang',
        'address': 'Lycee Classique de Dschang, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=800',
        'is_featured': True,
        'is_published': True,
    },
    {
        'title': 'Marche Solidaire pour l Education',
        'description': 'Rejoignez-nous pour une marche de 10km a travers Dschang. Les fonds collectes financeront les fournitures scolaires.',
        'short_description': 'Marche caritative de 10km pour financer les fournitures scolaires.',
        'event_date': timezone.now() + timedelta(days=60, hours=7),
        'location': 'Depart: Mairie de Dschang',
        'address': 'Mairie de Dschang, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Atelier Artisanat Traditionnel',
        'description': 'Initiation aux techniques artisanales ancestrales : tissage, poterie, sculpture sur bois.',
        'short_description': 'Decouvrez les techniques artisanales : tissage, poterie, sculpture.',
        'event_date': timezone.now() + timedelta(days=75, hours=9),
        'location': 'Centre Culturel FDTM',
        'address': 'Centre Culturel, Dschang',
        'image_url': 'https://images.unsplash.com/photo-1528312635006-8ea0bc49ec63?w=800',
        'is_featured': False,
        'is_published': True,
    },
    # PAST EVENTS
    {
        'title': 'Inauguration du Forage de Fongo-Tongo',
        'description': 'Inauguration officielle du nouveau forage apportant l eau potable a plus de 500 familles.',
        'short_description': 'Nouveau forage : eau potable pour 500 familles.',
        'event_date': timezone.now() - timedelta(days=30),
        'location': 'Fongo-Tongo',
        'address': 'Village de Fongo-Tongo, Region Ouest',
        'image_url': 'https://images.unsplash.com/photo-1541544741670-e3e3c4a91db3?w=800',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Campagne de Vaccination 2024',
        'description': 'Grande campagne de vaccination gratuite pour les enfants de 0 a 5 ans dans 8 villages.',
        'short_description': 'Vaccination gratuite pour les enfants dans 8 villages.',
        'event_date': timezone.now() - timedelta(days=60),
        'location': 'Plusieurs villages',
        'address': 'Region Ouest, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Festival Nkamsi 2024',
        'description': 'Edition 2024 du festival culturel avec plus de 2000 participants.',
        'short_description': 'Edition 2024 avec plus de 2000 participants.',
        'event_date': timezone.now() - timedelta(days=365),
        'location': 'Place du Marche, Dschang',
        'address': 'Dschang, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',
        'is_featured': False,
        'is_published': True,
    },
    {
        'title': 'Distribution de Kits Scolaires 2024',
        'description': 'Distribution de 200 kits scolaires aux eleves les plus defavorises.',
        'short_description': '200 kits scolaires distribues aux eleves.',
        'event_date': timezone.now() - timedelta(days=120),
        'location': 'Ecole Primaire de Foto',
        'address': 'Foto, Cameroun',
        'image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800',
        'is_featured': False,
        'is_published': True,
    },
]

for data in events:
    Event.objects.create(**data)
    print(f'Created: {data["title"]}')

print(f'Total events: {Event.objects.count()}')
print(f'Upcoming: {Event.objects.filter(event_date__gt=timezone.now()).count()}')
print(f'Past: {Event.objects.filter(event_date__lt=timezone.now()).count()}')
