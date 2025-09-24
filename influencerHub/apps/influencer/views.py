from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q, Count, Avg
from .models import Influencer, Category, SocialMediaAccount, Platform
from .forms import InfluencerRegistrationForm, SocialMediaAccountFormSet


class InfluencerListView(ListView):
    model = Influencer
    template_name = 'influencer/list.html'
    context_object_name = 'influencers'
    paginate_by = 12

    def get_queryset(self):
        queryset = Influencer.objects.select_related('category', 'status').prefetch_related('social_accounts')

        # Filtrage par catégorie
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)

        # Filtrage par plateforme
        platform = self.request.GET.get('platform')
        if platform:
            queryset = queryset.filter(social_accounts__platform_id=platform)

        # Recherche
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(full_name__icontains=search) |
                Q(niche_keywords__icontains=search)
            )

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['platforms'] = Platform.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['current_platform'] = self.request.GET.get('platform')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class InfluencerDetailView(DetailView):
    model = Influencer
    template_name = 'influencer/detail.html'
    context_object_name = 'influencer'


class InfluencerRegistrationView(SuccessMessageMixin, CreateView):
    model = Influencer
    form_class = InfluencerRegistrationForm
    template_name = 'influencer/register.html'
    success_url = reverse_lazy('influencer:success')
    success_message = "Votre inscription a été soumise avec succès ! Nous examinerons votre profil."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['social_formset'] = SocialMediaAccountFormSet(self.request.POST)
        else:
            context['social_formset'] = SocialMediaAccountFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        social_formset = context['social_formset']

        for form in social_formset:
            if form.is_valid() and form.has_changed():
                if not form.cleaned_data.get('following_count'):
                    form.instance.following_count = 0

        if social_formset.is_valid():
            self.object = form.save()
            social_formset.instance = self.object
            social_formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class InfluencerUpdateView(SuccessMessageMixin, UpdateView):
    model = Influencer
    form_class = InfluencerRegistrationForm
    template_name = 'influencer/edit.html'
    success_message = "Profil mis à jour avec succès !"

    def get_success_url(self):
        return reverse_lazy('influencer:detail', kwargs={'pk': self.object.pk})


class RegistrationSuccessView(TemplateView):
    template_name = 'influencer/success.html'
