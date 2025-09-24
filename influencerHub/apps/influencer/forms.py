from django import forms
from django.forms import inlineformset_factory
from .models import Influencer, SocialMediaAccount, Category, Platform

class InfluencerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Influencer
        fields = [
            'name', 'full_name', 'email', 'phone', 'bio',
            'profile_image', 'category', 'niche_keywords', 'location'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom public'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez-vous en quelques lignes...'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'niche_keywords': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mode, beauté, tech...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville, Pays'}),
        }

class SocialMediaAccountForm(forms.ModelForm):
    class Meta:
        model = SocialMediaAccount
        fields = ['platform', 'username', 'followers_count', 'engagement_rate']
        widgets = {
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '@username'}),
            'followers_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre d\'abonnés'}),
            'following_count': forms.NumberInput(attrs={'value': 0}),
            'engagement_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Taux d\'engagement (%)'}),
        }

SocialMediaAccountFormSet = inlineformset_factory(
    Influencer, SocialMediaAccount, form=SocialMediaAccountForm,
    extra=2, can_delete=True
)
