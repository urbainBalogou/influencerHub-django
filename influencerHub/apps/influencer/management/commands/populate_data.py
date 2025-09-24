import os
import django

from apps.influencer.models import *

from apps.influencer.models import InfluencerStatus, Category, Influencer, SocialMediaAccount, Platform

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'influencehub.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from influencer.models import *
from authentication.models import UserRole
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create platforms
        platforms_data = [
            {'name': 'INSTAGRAM', 'icon': 'fab fa-instagram'},
            {'name': 'TIKTOK', 'icon': 'fab fa-tiktok'},
            {'name': 'YOUTUBE', 'icon': 'fab fa-youtube'},
            {'name': 'TWITTER', 'icon': 'fab fa-twitter'},
            {'name': 'FACEBOOK', 'icon': 'fab fa-facebook'},
            {'name': 'LINKEDIN', 'icon': 'fab fa-linkedin'},
        ]

        for platform_data in platforms_data:
            Platform.objects.get_or_create(**platform_data)

        # Create statuses
        statuses_data = [
            {'name': 'ACTIVE', 'description': 'Influenceur actif', 'color': '#28a745'},
            {'name': 'PENDING', 'description': 'En attente de validation', 'color': '#ffc107'},
            {'name': 'VERIFIED', 'description': 'Profil vérifié', 'color': '#007bff'},
        ]

        for status_data in statuses_data:
            InfluencerStatus.objects.get_or_create(**status_data)

        # Create categories
        categories_data = [
            {'name': 'Mode & Beauté', 'description': 'Mode, beauté, cosmétiques', 'color': '#e83e8c'},
            {'name': 'Technologie', 'description': 'Tech, gadgets, innovations', 'color': '#6f42c1'},
            {'name': 'Fitness & Sport', 'description': 'Sport, fitness, bien-être', 'color': '#20c997'},
            {'name': 'Voyage', 'description': 'Voyage, aventure, découverte', 'color': '#fd7e14'},
            {'name': 'Cuisine', 'description': 'Cuisine, gastronomie, recettes', 'color': '#dc3545'},
            {'name': 'Gaming', 'description': 'Jeux vidéo, esport', 'color': '#6610f2'},
            {'name': 'Lifestyle', 'description': 'Style de vie, quotidien', 'color': '#17a2b8'},
        ]

        for category_data in categories_data:
            Category.objects.get_or_create(**category_data)

        # Create user roles
        roles_data = [
            {'name': 'ADMIN', 'description': 'Accès complet'},
            {'name': 'MANAGER', 'description': 'Gestion des influenceurs'},
            {'name': 'VIEWER', 'description': 'Consultation uniquement'},
        ]

        for role_data in roles_data:
            UserRole.objects.get_or_create(**role_data)

        # Create sample influencers
        sample_influencers = [
            {
                'name': 'Marie Dubois',
                'full_name': 'Marie Dubois',
                'email': 'marie.dubois@example.com',
                'phone': '+33123456789',
                'bio': 'Passionnée de mode et de beauté, je partage mes conseils styling et mes découvertes cosmétiques avec ma communauté.',
                'category': 'Mode & Beauté',
                'niche_keywords': 'mode, beauté, styling, cosmétiques',
                'location': 'Paris, France',
                'social_accounts': [
                    {'platform': 'INSTAGRAM', 'username': 'marie_style', 'followers': 150000, 'engagement': 4.2},
                    {'platform': 'TIKTOK', 'username': 'marie_beauty', 'followers': 80000, 'engagement': 6.1},
                ]
            },
            {
                'name': 'TechGuru Alex',
                'full_name': 'Alexandre Martin',
                'email': 'alex.martin@example.com',
                'bio': 'Expert en nouvelles technologies, tests de gadgets et conseils tech pour le grand public.',
                'category': 'Technologie',
                'niche_keywords': 'technologie, gadgets, smartphones, IA',
                'location': 'Lyon, France',
                'social_accounts': [
                    {'platform': 'YOUTUBE', 'username': 'TechGuruAlex', 'followers': 250000, 'engagement': 3.8},
                    {'platform': 'TWITTER', 'username': 'alextech', 'followers': 45000, 'engagement': 2.9},
                ]
            },
            {
                'name': 'Fitness Sarah',
                'full_name': 'Sarah Johnson',
                'email': 'sarah.johnson@example.com',
                'bio': 'Coach sportif certifiée, je vous accompagne dans votre transformation physique et mentale.',
                'category': 'Fitness & Sport',
                'niche_keywords': 'fitness, musculation, nutrition, wellness',
                'location': 'Nice, France',
                'social_accounts': [
                    {'platform': 'INSTAGRAM', 'username': 'fitness_sarah', 'followers': 95000, 'engagement': 5.2},
                    {'platform': 'YOUTUBE', 'username': 'SarahFitness', 'followers': 120000, 'engagement': 4.1},
                ]
            },
        ]

        for influencer_data in sample_influencers:
            # Get category
            category = Category.objects.get(name=influencer_data['category'])
            status = InfluencerStatus.objects.get(name='ACTIVE')

            # Create influencer
            social_accounts_data = influencer_data.pop('social_accounts')
            influencer_data['category'] = category
            influencer_data['status'] = status
            influencer_data['engagement_rate'] = Decimal(str(random.uniform(3.0, 7.0)))

            influencer, created = Influencer.objects.get_or_create(
                email=influencer_data['email'],
                defaults=influencer_data
            )

            if created:
                # Create social media accounts
                for account_data in social_accounts_data:
                    platform = Platform.objects.get(name=account_data['platform'])
                    SocialMediaAccount.objects.create(
                        influencer=influencer,
                        platform=platform,
                        username=account_data['username'],
                        followers_count=account_data['followers'],
                        following_count=random.randint(500, 2000),
                        posts_count=random.randint(100, 1000),
                        engagement_rate=Decimal(str(account_data['engagement'])),
                        is_verified=random.choice([True, False])
                    )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
