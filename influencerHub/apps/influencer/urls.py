from django.urls import path
from . import views

app_name = 'influencer'

urlpatterns = [
    path('', views.InfluencerListView.as_view(), name='list'),
    path('register/', views.InfluencerRegistrationView.as_view(), name='register'),
    path('<int:pk>/', views.InfluencerDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.InfluencerUpdateView.as_view(), name='edit'),
    path('success/', views.RegistrationSuccessView.as_view(), name='success'),
]