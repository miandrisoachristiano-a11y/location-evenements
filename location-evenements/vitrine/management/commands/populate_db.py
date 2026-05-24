import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from materiels.models import Materiel, CategorieMateriel
from evenements.models import TypeEvenement
from clients.models import Client
from locations.models import Location, LigneLocation
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Populate the database with fake data and online images'

    def handle(self, *args, **kwargs):
        fake = Faker('fr_FR')
        self.stdout.write("Nettoyage de la base de données...")
        
        # Nettoyage des données dépendantes pour éviter les erreurs d'intégrité
        LigneLocation.objects.all().delete()
        Location.objects.all().delete()
        Client.objects.all().delete()
        
        self.stdout.write("Génération des données avec images en ligne...")

        # 1. Catégories de matériel
        categories_names = ['Vaisselle', 'Mobilier', 'Sonorisation', 'Éclairage', 'Décoration', 'Tentes']
        categories = []
        for name in categories_names:
            cat, created = CategorieMateriel.objects.get_or_create(nom=name)
            categories.append(cat)
        self.stdout.write(f"- {len(categories)} catégories créées.")

        # 2. Matériels avec URLs d'images Unsplash
        materiels_data = {
            'Vaisselle': [
                ('Assiette porcelaine', 'https://images.unsplash.com/photo-1577106263724-2c8e03bfe9cf?auto=format&fit=crop&w=800&q=80'),
                ('Verre à vin Crystal', 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=800&q=80'),
            ],
            'Mobilier': [
                ('Chaise Napoléon blanche', 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'),
                ('Table ronde 10 pers', 'https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=800&q=80'),
            ],
            'Sonorisation': [
                ('Enceinte Active 500W', 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80'),
                ('Micro sans fil SHURE', 'https://images.unsplash.com/photo-1516280440614-37939bbacd81?auto=format&fit=crop&w=800&q=80'),
            ],
            'Éclairage': [
                ('Projecteur LED RGBW', 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80'),
                ('Guirlande Guinguette 10m', 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=800&q=80'),
            ],
            'Décoration': [
                ('Nappe blanche coton', 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80'),
                ('Vase Martini 70cm', 'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=800&q=80'),
            ],
            'Tentes': [
                ('Tente Barnum 3x3m', 'https://images.unsplash.com/photo-1523580494863-6f3031224b94?auto=format&fit=crop&w=800&q=80'),
                ('Chapiteau 6x12m', 'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80'),
            ]
        }

        materiels = []
        self.stdout.write("Nettoyage du matériel existant...")
        Materiel.objects.all().delete()
        
        for cat_name, items in materiels_data.items():
            cat = CategorieMateriel.objects.get(nom=cat_name)
            for item_name, img_url in items:
                mat, created = Materiel.objects.update_or_create(
                    nom=item_name,
                    categorie=cat,
                    defaults={
                        'description': f"Matériel de type {item_name} de haute qualité pour vos événements.",
                        'quantite_stock': random.randint(20, 200),
                        'prix_location_jour': random.randint(500, 50000),
                        'image_url': img_url,
                        'disponible': True
                    }
                )
                materiels.append(mat)
        self.stdout.write(f"- {len(materiels)} matériels mis à jour.")

        # 3. Types d'événements avec URLs d'images Unsplash
        self.stdout.write("Mise à jour des types d'événements (limité à 4)...")
        TypeEvenement.objects.all().delete()
        
        event_types_data = [
            ('Mariage', 'https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80'),
            ('Événement d\'Entreprise', 'https://images.unsplash.com/photo-1511578314322-379afb476865?auto=format&fit=crop&w=800&q=80'),
            ('Anniversaire', 'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=800&q=80'),
            ('Séminaire', 'https://images.unsplash.com/photo-1517457373958-b7bdd4587205?auto=format&fit=crop&w=800&q=80'),
        ]

        event_types = []
        for name, img_url in event_types_data:
            ev_type = TypeEvenement.objects.create(
                nom=name,
                description=f"Organisation complète pour votre {name.lower()}.",
                image_url=img_url
            )
            event_types.append(ev_type)
        self.stdout.write(f"- {len(event_types)} types d'événements mis à jour.")

        self.stdout.write(self.style.SUCCESS("Base de données mise à jour avec les images en ligne."))
