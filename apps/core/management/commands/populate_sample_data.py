"""
Management command to populate the database with realistic sample data.
Uses real images from Unsplash for visual content.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
import random
from datetime import timedelta

from apps.projects.models import ProjectCategory, Project, ProjectNeed, ProjectUpdate
from apps.articles.models import ArticleCategory, Article
from apps.core.models import SiteSettings, TeamMember, Testimonial, Partner, ImpactStat, FAQ, Newsletter


class Command(BaseCommand):
    help = 'Populate database with realistic sample data for FDTM NGO Platform'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for FDTM Platform...\n')
        
        # Create categories
        self.create_project_categories()
        self.create_article_categories()
        
        # Create projects
        self.create_projects()
        
        # Create articles
        self.create_articles()
        
        # Create core content
        self.create_site_settings()
        self.create_team_members()
        self.create_testimonials()
        self.create_impact_stats()
        self.create_faqs()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        self.stdout.write('Visit http://127.0.0.1:8001/ to see the site')
        self.stdout.write('Visit http://127.0.0.1:8001/admin/ to manage content')

    def create_project_categories(self):
        categories = [
            {'name': 'Santé', 'slug': 'sante', 'description': 'Projets de santé et accès aux soins', 'color': '#E53E3E', 'icon': 'health'},
            {'name': 'Éducation', 'slug': 'education', 'description': 'Projets éducatifs et bourses scolaires', 'color': '#3182CE', 'icon': 'education'},
            {'name': 'Culture', 'slug': 'culture', 'description': 'Préservation du patrimoine culturel', 'color': '#805AD5', 'icon': 'culture'},
            {'name': 'Aide Humanitaire', 'slug': 'humanitaire', 'description': 'Aide d\'urgence et soutien aux populations vulnérables', 'color': '#DD6B20', 'icon': 'humanitarian'},
        ]
        
        for cat in categories:
            ProjectCategory.objects.get_or_create(
                slug=cat['slug'],
                defaults=cat
            )
        self.stdout.write(f'  ✓ Created {len(categories)} project categories')

    def create_article_categories(self):
        categories = [
            {'name': 'Actualités', 'slug': 'actualites', 'description': 'Les dernières nouvelles de la fondation'},
            {'name': 'Histoires d\'impact', 'slug': 'histoires-impact', 'description': 'Témoignages et récits de transformation'},
            {'name': 'Événements', 'slug': 'evenements', 'description': 'Nos événements passés et à venir'},
            {'name': 'Communauté', 'slug': 'communaute', 'description': 'Nouvelles de nos villages partenaires'},
        ]
        
        for cat in categories:
            ArticleCategory.objects.get_or_create(
                slug=cat['slug'],
                defaults=cat
            )
        self.stdout.write(f'  ✓ Created {len(categories)} article categories')

    def create_projects(self):
        projects_data = [
            {
                'title': 'Centre de Santé de Foto',
                'slug': 'centre-sante-foto',
                'category_slug': 'sante',
                'short_description': 'Construction et équipement d\'un centre de santé communautaire à Foto pour servir plus de 5000 habitants.',
                'description': '''Le village de Foto, situé à 15 km de Dschang, souffre d'un manque cruel d'infrastructures de santé. Les habitants doivent parcourir des kilomètres pour accéder aux soins les plus basiques.

Notre projet vise à construire un centre de santé moderne équipé de :
- Une salle de consultation générale
- Une maternité avec 10 lits
- Un laboratoire d'analyses basiques
- Une pharmacie communautaire
- Un logement pour le personnel médical

Ce centre permettra de :
- Réduire la mortalité infantile et maternelle
- Offrir des soins préventifs (vaccinations, dépistages)
- Former des agents de santé communautaires
- Créer 8 emplois permanents dans le village''',
                'location': 'Foto, Dschang, Cameroun',
                'goal_amount': Decimal('45000.00'),
                'current_amount': Decimal('28750.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=800',
                'is_featured': True,
                'is_urgent': True,
                'status': 'active',
                'needs': [
                    {'title': 'Construction du bâtiment principal', 'need_type': 'financial', 'target_amount': Decimal('25000.00'), 'current_amount': Decimal('18000.00')},
                    {'title': 'Équipement médical', 'need_type': 'financial', 'target_amount': Decimal('15000.00'), 'current_amount': Decimal('8000.00')},
                    {'title': 'Lits d\'hôpital', 'need_type': 'material', 'quantity_needed': 15, 'quantity_received': 5},
                ],
                'updates': [
                    {'title': 'Pose de la première pierre', 'content': 'La cérémonie de pose de la première pierre a eu lieu en présence du chef du village et des autorités locales.', 'is_milestone': True},
                    {'title': 'Fondations terminées', 'content': 'Les travaux de fondation sont achevés. Les murs commencent à s\'élever !', 'is_milestone': False},
                ]
            },
            {
                'title': 'Bourses Scolaires 2024-2025',
                'slug': 'bourses-scolaires-2024',
                'category_slug': 'education',
                'short_description': 'Programme de bourses pour 50 élèves méritants issus de familles défavorisées de la région de Dschang.',
                'description': '''L'éducation est la clé du développement durable. Malheureusement, de nombreux enfants talentueux abandonnent l'école faute de moyens financiers.

Notre programme de bourses scolaires offre :
- Prise en charge des frais de scolarité
- Fournitures scolaires complètes
- Uniformes et chaussures
- Accompagnement pédagogique
- Suivi personnalisé tout au long de l'année

Critères de sélection :
- Excellence académique (moyenne supérieure à 12/20)
- Situation financière familiale difficile
- Motivation et projet d'avenir

Cette année, nous visons 50 bourses pour des élèves du primaire au lycée.''',
                'location': 'Dschang et environs, Cameroun',
                'goal_amount': Decimal('25000.00'),
                'current_amount': Decimal('15800.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=800',
                'is_featured': True,
                'is_urgent': False,
                'status': 'active',
                'needs': [
                    {'title': 'Bourses primaire (20 élèves)', 'need_type': 'financial', 'target_amount': Decimal('8000.00'), 'current_amount': Decimal('6000.00')},
                    {'title': 'Bourses collège (20 élèves)', 'need_type': 'financial', 'target_amount': Decimal('10000.00'), 'current_amount': Decimal('7000.00')},
                    {'title': 'Fournitures scolaires', 'need_type': 'material', 'quantity_needed': 50, 'quantity_received': 30},
                ],
                'updates': [
                    {'title': 'Sélection des boursiers terminée', 'content': '50 élèves méritants ont été sélectionnés après un processus rigoureux. Découvrez leurs profils !', 'is_milestone': True},
                ]
            },
            {
                'title': 'Bibliothèque Communautaire de Bafou',
                'slug': 'bibliotheque-bafou',
                'category_slug': 'education',
                'short_description': 'Création d\'une bibliothèque et espace numérique pour les jeunes de Bafou et villages environnants.',
                'description': '''Bafou est l'un des plus grands villages de la région, mais il ne dispose d'aucune bibliothèque. Les élèves n'ont pas accès aux livres en dehors de l'école.

Notre projet comprend :
- Rénovation d'un bâtiment communautaire existant
- Acquisition de 3000 livres (manuels, romans, encyclopédies)
- Installation de 10 ordinateurs avec internet
- Formation de bibliothécaires bénévoles
- Programme d'alphabétisation pour adultes

Impact attendu :
- 1500 jeunes bénéficiaires directs
- Amélioration des résultats scolaires
- Réduction de l'analphabétisme chez les adultes
- Accès au numérique pour tous''',
                'location': 'Bafou, Dschang, Cameroun',
                'goal_amount': Decimal('18000.00'),
                'current_amount': Decimal('5200.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800',
                'is_featured': False,
                'is_urgent': False,
                'status': 'active',
                'needs': [
                    {'title': 'Rénovation du bâtiment', 'need_type': 'financial', 'target_amount': Decimal('8000.00'), 'current_amount': Decimal('3000.00')},
                    {'title': 'Livres', 'need_type': 'material', 'quantity_needed': 3000, 'quantity_received': 450},
                    {'title': 'Ordinateurs', 'need_type': 'material', 'quantity_needed': 10, 'quantity_received': 2},
                ],
                'updates': []
            },
            {
                'title': 'Festival Culturel Nkam\'si',
                'slug': 'festival-nkamsi',
                'category_slug': 'culture',
                'short_description': 'Organisation du festival annuel célébrant le patrimoine culturel Bamiléké pour préserver les traditions ancestrales.',
                'description': '''Le festival Nkam'si (qui signifie "notre héritage" en langue locale) est un événement annuel visant à préserver et transmettre la richesse culturelle Bamiléké aux jeunes générations.

Au programme :
- Danses traditionnelles et concerts
- Expositions d'artisanat local
- Contes et légendes racontés par les anciens
- Compétitions de cuisine traditionnelle
- Transmission des savoirs ancestraux

Ce festival permet de :
- Renforcer l'identité culturelle des jeunes
- Créer des revenus pour les artisans locaux
- Favoriser le tourisme culturel
- Documenter les traditions en voie de disparition''',
                'location': 'Dschang, Cameroun',
                'goal_amount': Decimal('12000.00'),
                'current_amount': Decimal('8900.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800',
                'is_featured': True,
                'is_urgent': False,
                'status': 'active',
                'needs': [
                    {'title': 'Logistique et scène', 'need_type': 'financial', 'target_amount': Decimal('5000.00'), 'current_amount': Decimal('4500.00')},
                    {'title': 'Costumes traditionnels', 'need_type': 'material', 'quantity_needed': 50, 'quantity_received': 35},
                ],
                'updates': [
                    {'title': 'Dates confirmées : 15-17 Mars 2025', 'content': 'Le festival se tiendra du 15 au 17 mars 2025 sur la place du marché de Dschang.', 'is_milestone': True},
                ]
            },
            {
                'title': 'Aide d\'Urgence aux Déplacés',
                'slug': 'aide-urgence-deplaces',
                'category_slug': 'humanitaire',
                'short_description': 'Assistance humanitaire pour les familles déplacées par les conflits dans les régions anglophones.',
                'description': '''Depuis 2017, le conflit dans les régions anglophones du Cameroun a provoqué le déplacement de centaines de milliers de personnes. Dschang accueille de nombreuses familles réfugiées.

Notre programme d'aide d'urgence comprend :
- Distribution de kits alimentaires mensuels
- Fourniture d'articles de première nécessité (couvertures, ustensiles, vêtements)
- Soutien psychologique aux traumatisés
- Aide à la scolarisation des enfants déplacés
- Accompagnement vers l'autonomie

Nous assistons actuellement 120 familles, soit environ 600 personnes dont 250 enfants.''',
                'location': 'Dschang et environs, Cameroun',
                'goal_amount': Decimal('35000.00'),
                'current_amount': Decimal('22400.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=800',
                'is_featured': True,
                'is_urgent': True,
                'status': 'active',
                'needs': [
                    {'title': 'Kits alimentaires (3 mois)', 'need_type': 'financial', 'target_amount': Decimal('18000.00'), 'current_amount': Decimal('14000.00')},
                    {'title': 'Frais de scolarité enfants', 'need_type': 'financial', 'target_amount': Decimal('12000.00'), 'current_amount': Decimal('6000.00')},
                    {'title': 'Vêtements et couvertures', 'need_type': 'material', 'quantity_needed': 200, 'quantity_received': 85},
                ],
                'updates': [
                    {'title': 'Distribution de décembre terminée', 'content': '120 familles ont reçu leurs kits alimentaires de décembre. Merci à tous les donateurs !', 'is_milestone': False},
                ]
            },
            {
                'title': 'Jardin Médicinal Traditionnel',
                'slug': 'jardin-medicinal',
                'category_slug': 'sante',
                'short_description': 'Création d\'un jardin de plantes médicinales pour préserver les savoirs thérapeutiques traditionnels.',
                'description': '''Les guérisseurs traditionnels Bamiléké possèdent un savoir ancestral sur les plantes médicinales. Ce patrimoine disparaît avec les anciens.

Notre projet vise à :
- Créer un jardin conservatoire de 500 espèces médicinales
- Documenter les usages traditionnels avec les tradipraticiens
- Former les jeunes à la phytothérapie
- Produire des remèdes naturels à faible coût
- Créer un centre de formation

Impact :
- Préservation du patrimoine médicinal
- Complémentarité avec la médecine moderne
- Création d'emplois locaux
- Accès aux soins pour les plus démunis''',
                'location': 'Foréké-Dschang, Cameroun',
                'goal_amount': Decimal('15000.00'),
                'current_amount': Decimal('4200.00'),
                'featured_image_url': 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=800',
                'is_featured': False,
                'is_urgent': False,
                'status': 'active',
                'needs': [
                    {'title': 'Aménagement du terrain', 'need_type': 'financial', 'target_amount': Decimal('6000.00'), 'current_amount': Decimal('2500.00')},
                    {'title': 'Plants et semences', 'need_type': 'material', 'quantity_needed': 500, 'quantity_received': 120},
                ],
                'updates': []
            },
        ]

        for p_data in projects_data:
            category = ProjectCategory.objects.get(slug=p_data['category_slug'])
            
            project, created = Project.objects.get_or_create(
                slug=p_data['slug'],
                defaults={
                    'title': p_data['title'],
                    'category': category,
                    'short_description': p_data['short_description'],
                    'description': p_data['description'],
                    'location': p_data['location'],
                    'goal_amount': p_data['goal_amount'],
                    'current_amount': p_data['current_amount'],
                    'featured_image_url': p_data['featured_image_url'],
                    'is_featured': p_data['is_featured'],
                    'is_urgent': p_data['is_urgent'],
                    'status': p_data['status'],
                    'start_date': timezone.now().date() - timedelta(days=random.randint(30, 180)),
                }
            )
            
            if created:
                # Create needs
                for need in p_data.get('needs', []):
                    ProjectNeed.objects.create(
                        project=project,
                        title=need['title'],
                        need_type=need['need_type'],
                        target_amount=need.get('target_amount', Decimal('0')),
                        current_amount=need.get('current_amount', Decimal('0')),
                        quantity_needed=need.get('quantity_needed', 0),
                        quantity_received=need.get('quantity_received', 0),
                    )
                
                # Create updates
                for i, update in enumerate(p_data.get('updates', [])):
                    ProjectUpdate.objects.create(
                        project=project,
                        title=update['title'],
                        content=update['content'],
                        is_milestone=update['is_milestone'],
                        created_at=timezone.now() - timedelta(days=(len(p_data['updates']) - i) * 15)
                    )
        
        self.stdout.write(f'  ✓ Created {len(projects_data)} projects with needs and updates')

    def create_articles(self):
        articles_data = [
            {
                'title': 'Inauguration du puits de Fongo-Tongo : l\'eau coule enfin !',
                'slug': 'inauguration-puits-fongo-tongo',
                'category_slug': 'histoires-impact',
                'excerpt': 'Après 6 mois de travaux, le village de Fongo-Tongo dispose enfin d\'un accès à l\'eau potable. Retour sur ce projet qui change la vie de 800 familles.',
                'content': '''<p>C'était un jour de fête à Fongo-Tongo. Sous un soleil radieux, les habitants du village se sont rassemblés autour du nouveau puits, fruit de plusieurs mois de travail et de générosité.</p>

<h2>Un besoin vital enfin comblé</h2>
<p>Avant ce puits, les femmes et les enfants devaient marcher plus de 3 kilomètres pour puiser de l'eau dans la rivière. Une eau souvent contaminée, source de nombreuses maladies.</p>

<p>"Mes enfants tombaient malades au moins une fois par mois à cause de l'eau", raconte Maman Jeanne, 45 ans, mère de 6 enfants. "Maintenant, ils sont en bonne santé. C'est un miracle !"</p>

<h2>Un projet communautaire</h2>
<p>Ce projet a été rendu possible grâce à la mobilisation de la diaspora camerounaise en Europe et aux dons de particuliers du monde entier. Les habitants du village ont contribué par leur travail : creusement, transport de matériaux, construction de la margelle.</p>

<p>Le chef du village, Sa Majesté Fomekong II, a exprimé sa gratitude : "La FDTM a compris que le développement doit venir de nous, avec nous. Ils ne nous ont pas juste donné un puits, ils nous ont aidés à le construire ensemble."</p>

<h2>L'impact au quotidien</h2>
<ul>
<li>800 familles ont désormais accès à l'eau potable</li>
<li>Les cas de maladies hydriques ont chuté de 75%</li>
<li>Les femmes économisent 3 heures par jour</li>
<li>Les enfants sont plus assidus à l'école</li>
</ul>

<p>Ce puits n'est qu'un début. La FDTM prévoit d'équiper 5 autres villages de la région d'ici 2026.</p>''',
                'featured_image_url': 'https://images.unsplash.com/photo-1594398901394-4e34c8f2c2e9?w=800',
                'author_name': 'Marie Nguemo',
                'reading_time': 4,
                'is_featured': True,
            },
            {
                'title': 'Rentrée scolaire 2024 : 50 nouveaux boursiers !',
                'slug': 'rentree-scolaire-2024-boursiers',
                'category_slug': 'actualites',
                'excerpt': 'Cette année, 50 élèves méritants ont reçu leur bourse de la FDTM. Découvrez ces jeunes talents qui construisent l\'avenir du Cameroun.',
                'content': '''<p>La rentrée scolaire 2024-2025 est une étape importante pour 50 jeunes de la région de Dschang. Grâce au programme de bourses de la FDTM, ils peuvent poursuivre leurs études malgré les difficultés financières de leurs familles.</p>

<h2>Des profils inspirants</h2>
<p>Parmi les boursiers de cette année, citons Ornella, 14 ans, première de sa classe depuis le CE2 : "Je rêve de devenir médecin pour soigner les gens de mon village. Sans cette bourse, j'aurais dû arrêter l'école pour aider ma mère au champ."</p>

<p>Ou encore Christian, 17 ans, passionné d'informatique : "Je veux créer des applications pour aider les agriculteurs camerounais. La FDTM me donne cette chance."</p>

<h2>Un accompagnement complet</h2>
<p>La bourse FDTM ne se limite pas aux frais de scolarité. Elle comprend :</p>
<ul>
<li>Prise en charge complète des frais d'inscription</li>
<li>Kit scolaire complet (cahiers, stylos, sac)</li>
<li>Deux uniformes par an</li>
<li>Suivi trimestriel par un tuteur</li>
<li>Soutien scolaire si nécessaire</li>
</ul>

<h2>Des résultats probants</h2>
<p>Depuis 2019, le programme a soutenu plus de 200 élèves. Le taux de réussite aux examens atteint 92%, contre 65% en moyenne nationale.</p>

<p>Trois anciens boursiers sont aujourd'hui à l'université, dont deux en médecine. La preuve que l'investissement dans l'éducation porte ses fruits !</p>''',
                'featured_image_url': 'https://images.unsplash.com/photo-1427504494785-3a9ca7044f45?w=800',
                'author_name': 'Paul Kemajou',
                'reading_time': 3,
                'is_featured': True,
            },
            {
                'title': 'Le Festival Nkam\'si revient en mars 2025 !',
                'slug': 'festival-nkamsi-mars-2025',
                'category_slug': 'evenements',
                'excerpt': 'La 5ème édition du festival culturel Nkam\'si se tiendra du 15 au 17 mars 2025 à Dschang. Au programme : danses, artisanat et gastronomie traditionnelle.',
                'content': '''<p>Après le succès de l'édition 2024 qui avait rassemblé plus de 2000 visiteurs, le festival Nkam'si revient pour une 5ème édition encore plus ambitieuse.</p>

<h2>Au programme</h2>
<p><strong>Vendredi 15 mars - Journée d'ouverture</strong></p>
<ul>
<li>14h : Cérémonie d'ouverture par les chefs traditionnels</li>
<li>16h : Parade des groupes folkloriques</li>
<li>20h : Grand concert de musique traditionnelle</li>
</ul>

<p><strong>Samedi 16 mars - Journée des arts</strong></p>
<ul>
<li>9h-18h : Marché artisanal (sculptures, tissages, poteries)</li>
<li>10h : Démonstrations de tissage du Ndop</li>
<li>15h : Compétition de danse Tso</li>
<li>20h : Veillée de contes avec les anciens</li>
</ul>

<p><strong>Dimanche 17 mars - Journée gastronomique</strong></p>
<ul>
<li>10h : Concours de cuisine traditionnelle</li>
<li>14h : Dégustation géante</li>
<li>17h : Cérémonie de clôture</li>
</ul>

<h2>Pourquoi y participer ?</h2>
<p>Le festival Nkam'si est bien plus qu'un événement culturel. C'est une occasion unique de :</p>
<ul>
<li>Découvrir la richesse de la culture Bamiléké</li>
<li>Soutenir les artisans locaux</li>
<li>Rencontrer les acteurs du développement local</li>
<li>Contribuer à la préservation du patrimoine</li>
</ul>

<p>Entrée libre. Restauration sur place.</p>''',
                'featured_image_url': 'https://images.unsplash.com/photo-1533174072545-7a4b6ad7a6c3?w=800',
                'author_name': 'Équipe FDTM',
                'reading_time': 3,
                'is_featured': False,
            },
            {
                'title': 'Témoignage : Maman Rose, guérisseuse traditionnelle',
                'slug': 'temoignage-maman-rose-guerisseuse',
                'category_slug': 'communaute',
                'excerpt': 'À 78 ans, Maman Rose transmet son savoir sur les plantes médicinales aux jeunes du village. Un patrimoine inestimable à préserver.',
                'content': '''<p>Dans sa petite case entourée de plantes, Maman Rose nous accueille avec un sourire bienveillant. À 78 ans, elle est l'une des dernières guérisseuses traditionnelles de Foréké-Dschang.</p>

<h2>"Les plantes ont des secrets"</h2>
<p>"Ma mère m'a appris les plantes quand j'avais 10 ans", raconte-t-elle en montrant son jardin. "Chaque feuille, chaque racine a un pouvoir. Il faut savoir les écouter."</p>

<p>Pendant des décennies, Maman Rose a soigné les habitants du village avec ses remèdes naturels : décoctions pour le paludisme, cataplasmes pour les plaies, infusions pour les maux de ventre.</p>

<h2>Un savoir menacé</h2>
<p>"Les jeunes ne s'intéressent plus à ça", déplore-t-elle. "Ils veulent les médicaments de la pharmacie. Mais quand la pharmacie est à 20 km et qu'on n'a pas d'argent, ce sont les plantes qui sauvent."</p>

<p>C'est pourquoi le projet de jardin médicinal de la FDTM lui tient à cœur. "Si on ne transmet pas ce savoir, il mourra avec nous. Avec ce jardin, les jeunes pourront apprendre."</p>

<h2>La relève se prépare</h2>
<p>Trois jeunes du village ont commencé à suivre les enseignements de Maman Rose. Parmi eux, Samuel, 22 ans, étudiant en biologie : "Je veux documenter scientifiquement ces savoirs. C'est une richesse que le monde entier devrait connaître."</p>

<p>Avec le soutien de la FDTM, le jardin médicinal permettra de former une nouvelle génération de praticiens et de préserver ce patrimoine unique.</p>''',
                'featured_image_url': 'https://images.unsplash.com/photo-1509099836639-18ba1795216d?w=800',
                'author_name': 'Marie Nguemo',
                'reading_time': 5,
                'is_featured': True,
            },
            {
                'title': 'Bilan 2024 : une année de transformation',
                'slug': 'bilan-2024-transformation',
                'category_slug': 'actualites',
                'excerpt': 'Retour sur les réalisations de la FDTM en 2024 : 6 projets achevés, 120 familles aidées, et des milliers de vies transformées.',
                'content': '''<p>L'année 2024 a été exceptionnelle pour la Fondation Denise Time Mafodom. Grâce à la générosité de nos donateurs et à l'engagement de notre équipe sur le terrain, nous avons atteint des résultats remarquables.</p>

<h2>Les chiffres clés</h2>
<ul>
<li><strong>6 projets achevés</strong> (2 puits, 1 école rénovée, 3 distributions humanitaires)</li>
<li><strong>50 bourses scolaires</strong> attribuées</li>
<li><strong>120 familles déplacées</strong> soutenues mensuellement</li>
<li><strong>2 500 consultations médicales</strong> lors de nos campagnes de santé</li>
<li><strong>85 000 € collectés</strong> grâce à vos dons</li>
</ul>

<h2>Nos plus belles réussites</h2>
<p><strong>Le puits de Fongo-Tongo</strong> : 800 familles ont désormais accès à l'eau potable.</p>
<p><strong>La rénovation de l'école de Balessing</strong> : 350 élèves étudient dans des salles de classe dignes.</p>
<p><strong>Le festival Nkam'si</strong> : 2000 visiteurs, 50 artisans, et un patrimoine célébré.</p>

<h2>Perspectives pour 2025</h2>
<p>L'année prochaine s'annonce tout aussi ambitieuse avec :</p>
<ul>
<li>La construction du centre de santé de Foto</li>
<li>L'ouverture de la bibliothèque de Bafou</li>
<li>L'extension du programme de bourses à 75 élèves</li>
<li>Le lancement du jardin médicinal</li>
</ul>

<p>Merci à tous ceux qui nous font confiance. Ensemble, nous construisons un avenir meilleur pour les communautés de Dschang.</p>''',
                'featured_image_url': 'https://images.unsplash.com/photo-1469571486292-0ba58a3f068b?w=800',
                'author_name': 'Équipe FDTM',
                'reading_time': 4,
                'is_featured': False,
            },
        ]

        for a_data in articles_data:
            category = ArticleCategory.objects.get(slug=a_data['category_slug'])
            
            Article.objects.get_or_create(
                slug=a_data['slug'],
                defaults={
                    'title': a_data['title'],
                    'category': category,
                    'excerpt': a_data['excerpt'],
                    'content': a_data['content'],
                    'featured_image_url': a_data['featured_image_url'],
                    'author_name': a_data['author_name'],
                    'reading_time': a_data['reading_time'],
                    'is_featured': a_data['is_featured'],
                    'status': 'published',
                    'published_date': timezone.now() - timedelta(days=random.randint(1, 60)),
                }
            )
        
        self.stdout.write(f'  ✓ Created {len(articles_data)} articles')

    def create_site_settings(self):
        SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Fondation Denise Time Mafodom',
                'tagline': 'Construire un avenir meilleur, main dans la main',
                'contact_email': 'contact@fdtm.org',
                'contact_phone': '+237 6 90 00 00 00',
                'address': 'Dschang, Région de l\'Ouest, Cameroun',
                'mission_text': 'Allumer l\'espoir, autonomiser les vies et transformer les communautés par notre humanité partagée.',
                'vision_text': 'Un monde uni par la compassion, où chaque communauté s\'épanouit dans la dignité et avec un but.',
                'facebook_url': 'https://facebook.com/fdtm.org',
                'instagram_url': 'https://instagram.com/fdtm_org',
                'twitter_url': 'https://twitter.com/fdtm_org',
                'linkedin_url': 'https://linkedin.com/company/fdtm',
            }
        )
        self.stdout.write('  ✓ Created site settings')

    def create_team_members(self):
        team = [
            {
                'name': 'Dr. Emmanuel Tagne',
                'title': 'Directeur Général',
                'bio': 'Médecin de formation, Emmanuel a fondé la FDTM en 2018 après 15 ans de pratique dans les zones rurales du Cameroun.',
                'photo_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400',
                'email': 'emmanuel@fdtm.org',
                'order': 1,
            },
            {
                'name': 'Marie-Claire Nguemo',
                'title': 'Directrice des Programmes',
                'bio': 'Spécialiste du développement communautaire, Marie-Claire coordonne tous les projets sur le terrain depuis 2019.',
                'photo_url': 'https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400',
                'email': 'marie@fdtm.org',
                'order': 2,
            },
            {
                'name': 'Paul Kemajou',
                'title': 'Responsable Communication',
                'bio': 'Journaliste et photographe, Paul raconte les histoires de transformation de nos bénéficiaires.',
                'photo_url': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400',
                'email': 'paul@fdtm.org',
                'order': 3,
            },
            {
                'name': 'Sandrine Fokou',
                'title': 'Responsable Éducation',
                'bio': 'Enseignante pendant 10 ans, Sandrine gère le programme de bourses et le suivi des élèves.',
                'photo_url': 'https://images.unsplash.com/photo-1580489944761-15a19d654956?w=400',
                'email': 'sandrine@fdtm.org',
                'order': 4,
            },
        ]
        
        for member in team:
            TeamMember.objects.get_or_create(
                name=member['name'],
                defaults={
                    'title': member['title'],
                    'bio': member['bio'],
                    'photo_url': member['photo_url'],
                    'email': member['email'],
                    'order': member['order'],
                    'is_active': True,
                }
            )
        self.stdout.write(f'  ✓ Created {len(team)} team members')

    def create_testimonials(self):
        testimonials = [
            {
                'name': 'Maman Jeanne',
                'location': 'Fongo-Tongo',
                'quote': 'Depuis que le puits est là, mes enfants ne tombent plus malades. Je peux enfin travailler au lieu de marcher des heures pour chercher l\'eau.',
                'is_featured': True,
            },
            {
                'name': 'Christian Ngoufack',
                'location': 'Dschang',
                'quote': 'La bourse de la FDTM m\'a permis de continuer mes études. Aujourd\'hui je suis en première année de médecine. Un jour, je soignerai les gens de mon village.',
                'is_featured': True,
            },
            {
                'name': 'Chef Fomekong II',
                'location': 'Foto',
                'quote': 'La FDTM ne nous aide pas comme des assistés. Elle nous accompagne pour que nous construisions notre propre développement. C\'est ça la vraie solidarité.',
                'is_featured': True,
            },
        ]
        
        for t in testimonials:
            Testimonial.objects.get_or_create(
                name=t['name'],
                defaults={
                    'location': t['location'],
                    'quote': t['quote'],
                    'is_featured': t['is_featured'],
                    'is_active': True,
                }
            )
        self.stdout.write(f'  ✓ Created {len(testimonials)} testimonials')

    def create_impact_stats(self):
        stats = [
            {'title': 'Familles aidées', 'value': 520, 'suffix': '+', 'icon': 'users', 'order': 1},
            {'title': 'Projets réalisés', 'value': 15, 'suffix': '', 'icon': 'project', 'order': 2},
            {'title': 'Bourses attribuées', 'value': 200, 'suffix': '+', 'icon': 'education', 'order': 3},
            {'title': 'Taux d\'utilisation des dons', 'value': 92, 'suffix': '%', 'icon': 'chart', 'order': 4},
        ]
        
        for stat in stats:
            ImpactStat.objects.get_or_create(
                title=stat['title'],
                defaults={
                    'value': stat['value'],
                    'suffix': stat['suffix'],
                    'icon': stat['icon'],
                    'order': stat['order'],
                    'is_active': True,
                }
            )
        self.stdout.write(f'  ✓ Created {len(stats)} impact stats')

    def create_faqs(self):
        faqs = [
            {
                'question': 'Comment mes dons sont-ils utilisés ?',
                'answer': '92% de vos dons vont directement aux projets sur le terrain. Les 8% restants couvrent les frais de fonctionnement (communication, comptabilité, déplacements). Nous publions un rapport financier annuel détaillé.',
                'order': 1,
            },
            {
                'question': 'Puis-je visiter les projets ?',
                'answer': 'Oui ! Nous organisons des missions de terrain pour les donateurs qui souhaitent voir l\'impact de leur contribution. Contactez-nous pour planifier une visite.',
                'order': 2,
            },
            {
                'question': 'Comment puis-je devenir bénévole ?',
                'answer': 'Nous recherchons des bénévoles pour des missions sur le terrain (2 semaines minimum) ou pour du soutien à distance (traduction, communication, collecte de fonds). Envoyez-nous votre CV et motivations.',
                'order': 3,
            },
            {
                'question': 'Les dons sont-ils déductibles des impôts ?',
                'answer': 'Oui, la FDTM est une association reconnue d\'utilité publique. En France, vos dons sont déductibles à 66% de votre impôt sur le revenu. Un reçu fiscal vous est envoyé automatiquement.',
                'order': 4,
            },
            {
                'question': 'Comment suivre l\'avancement des projets ?',
                'answer': 'Nous envoyons des newsletters trimestrielles avec des mises à jour détaillées. Vous pouvez aussi suivre nos réseaux sociaux et consulter la page de chaque projet sur notre site.',
                'order': 5,
            },
        ]
        
        for faq in faqs:
            FAQ.objects.get_or_create(
                question=faq['question'],
                defaults={
                    'answer': faq['answer'],
                    'order': faq['order'],
                    'is_active': True,
                }
            )
        self.stdout.write(f'  ✓ Created {len(faqs)} FAQs')
