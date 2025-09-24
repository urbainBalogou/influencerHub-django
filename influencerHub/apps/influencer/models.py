from django.db import models
from decimal import Decimal


class Platform(models.Model):
    PLATFORM_CHOICES = [
        ('INSTAGRAM', 'Instagram'),
        ('TIKTOK', 'TikTok'),
        ('YOUTUBE', 'YouTube'),
        ('TWITTER', 'Twitter'),
        ('FACEBOOK', 'Facebook'),
        ('LINKEDIN', 'LinkedIn'),
    ]

    name = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Classe CSS pour l'icône")

    class Meta:
        verbose_name = "Plateforme"
        verbose_name_plural = "Plateformes"

    def __str__(self):
        return self.get_name_display()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default="#007bff", help_text="Couleur hex")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name


class InfluencerStatus(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Actif'),
        ('INACTIVE', 'Inactif'),
        ('PENDING', 'En attente'),
        ('VERIFIED', 'Vérifié'),
        ('REJECTED', 'Rejeté'),
    ]

    name = models.CharField(max_length=20, choices=STATUS_CHOICES, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default="#28a745")

    class Meta:
        verbose_name = "Statut influenceur"
        verbose_name_plural = "Statuts influenceurs"

    def __str__(self):
        return self.get_name_display()


class Influencer(models.Model):
    # Informations de base
    name = models.CharField(max_length=100, verbose_name="Nom")
    full_name = models.CharField(max_length=150, verbose_name="Nom complet")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    bio = models.TextField(blank=True, verbose_name="Biographie")

    # Informations professionnelles
    profile_image = models.ImageField(upload_to='influencers/profiles/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Catégorie")
    niche_keywords = models.TextField(blank=True, help_text="Mots-clés séparés par des virgules")
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, verbose_name="Localisation")

    # Statut et dates
    status = models.ForeignKey(InfluencerStatus, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Modifié le")

    class Meta:
        verbose_name = "Influenceur"
        verbose_name_plural = "Influenceurs"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def calculate_engagement(self):
        """Calcule le taux d'engagement moyen sur toutes les plateformes"""
        accounts = self.social_accounts.all()
        if not accounts:
            return Decimal('0.00')

        total_engagement = sum(acc.engagement_rate or 0 for acc in accounts)
        return Decimal(total_engagement) / len(accounts)

    def get_total_reach(self):
        """Calcule la portée totale sur toutes les plateformes"""
        return sum(acc.followers_count for acc in self.social_accounts.all())

    def validate(self):
        """Valide les données de l'influenceur"""
        errors = []

        if self.engagement_rate and (self.engagement_rate < 0 or self.engagement_rate > 100):
            errors.append("Le taux d'engagement doit être entre 0 et 100%")

        return errors


class SocialMediaAccount(models.Model):
    influencer = models.ForeignKey(Influencer, related_name='social_accounts', on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name="Plateforme")
    username = models.CharField(max_length=100, verbose_name="Nom d'utilisateur")
    followers_count = models.PositiveIntegerField(verbose_name="Nombre d'abonnés")
    following_count = models.PositiveIntegerField(
        default=0,
        null=True,
        blank=True
    )
    posts_count = models.PositiveIntegerField(verbose_name="Nombre de publications")
    engagement_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name="Compte vérifié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compte réseau social"
        verbose_name_plural = "Comptes réseaux sociaux"
        unique_together = ['influencer', 'platform']

    def __str__(self):
        return f"{self.influencer.name} - {self.platform.get_name_display()}"

    def update_metrics(self):
        """Met à jour les métriques du compte"""
        # Logique pour récupérer les nouvelles métriques via API
        pass

    def validate(self):
        """Valide les données du compte"""
        if self.engagement_rate and self.engagement_rate > 100:
            raise ValueError("Le taux d'engagement ne peut pas dépasser 100%")

    @property
    def verified_accounts_count(self):
        return self.social_accounts.filter(is_verified=True).count()