from django.contrib import admin
from django.db.models import Count, Avg, Sum
from django.utils.html import format_html
from .models import Influencer, Category, SocialMediaAccount, InfluencerStatus, Platform


class SocialMediaAccountInline(admin.TabularInline):
    model = SocialMediaAccount
    extra = 1
    fields = ['platform', 'username', 'followers_count', 'engagement_rate', 'is_verified']


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']


@admin.register(InfluencerStatus)
class InfluencerStatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'color_preview']
    search_fields = ['name', 'description']

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 50%;"></div>',
            obj.color
        )

    color_preview.short_description = 'Couleur'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'influencer_count', 'color_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Couleur'

    def influencer_count(self, obj):
        return obj.influencer_count
    influencer_count.short_description = 'Nb. influenceurs'

    def get_queryset(self, request):
        # ✅ Indentation correcte
        return super().get_queryset(request).annotate(
            influencer_count=Count('influencers')  # related_name de ForeignKey
        )



@admin.register(Influencer)
class InfluencerAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'email', 'category', 'status', 'total_followers',
        'avg_engagement', 'platform_count', 'created_at'
    ]
    list_filter = [
        'status', 'category', 'created_at', 'updated_at',
        'social_accounts__platform', 'social_accounts__is_verified'
    ]
    search_fields = ['name', 'full_name', 'email', 'niche_keywords']
    readonly_fields = ['created_at', 'updated_at', 'total_followers', 'avg_engagement']
    inlines = [SocialMediaAccountInline]

    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'full_name', 'email', 'phone', 'bio', 'profile_image')
        }),
        ('Informations professionnelles', {
            'fields': ('category', 'niche_keywords', 'engagement_rate', 'location')
        }),
        ('Statut et suivi', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
        ('Métriques calculées', {
            'fields': ('total_followers', 'avg_engagement'),
            'classes': ('collapse',)
        })
    )

    actions = ['mark_as_verified', 'mark_as_active', 'export_to_csv']

    def total_followers(self, obj):
        total = obj.social_accounts.aggregate(Sum('followers_count'))['followers_count__sum']
        return f"{total:,}" if total else "0"

    total_followers.short_description = 'Abonnés totaux'
    total_followers.admin_order_field = 'total_followers_count'

    def avg_engagement(self, obj):
        avg = obj.social_accounts.aggregate(Avg('engagement_rate'))['engagement_rate__avg']
        return f"{avg:.2f}%" if avg else "N/A"

    avg_engagement.short_description = 'Engagement moyen'

    def platform_count(self, obj):
        return obj.social_accounts.count()

    platform_count.short_description = 'Plateformes'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'social_accounts', 'category', 'status'
        ).annotate(
            total_followers_count=Sum('social_accounts__followers_count'),
            avg_engagement_rate=Avg('social_accounts__engagement_rate')
        )

    def mark_as_verified(self, request, queryset):
        verified_status = InfluencerStatus.objects.get(name='VERIFIED')
        updated = queryset.update(status=verified_status)
        self.message_user(request, f'{updated} influenceurs marqués comme vérifiés.')

    mark_as_verified.short_description = "Marquer comme vérifié"

    def mark_as_active(self, request, queryset):
        active_status = InfluencerStatus.objects.get(name='ACTIVE')
        updated = queryset.update(status=active_status)
        self.message_user(request, f'{updated} influenceurs marqués comme actifs.')

    mark_as_active.short_description = "Marquer comme actif"


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = [
        'influencer', 'platform', 'username', 'followers_count',
        'engagement_rate', 'is_verified', 'updated_at'
    ]
    list_filter = ['platform', 'is_verified', 'created_at']
    search_fields = ['username', 'influencer__name', 'influencer__email']
    readonly_fields = ['created_at', 'updated_at']
