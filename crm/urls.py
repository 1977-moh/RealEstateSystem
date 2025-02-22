from django.urls import path
from .views import ClientListView, ClientDetailView, LeadListView, AIRecommendationView

app_name = 'crm'

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='client-list'),
    path('clients/<uuid:pk>/', ClientDetailView.as_view(), name='client-detail'),
    path('leads/', LeadListView.as_view(), name='lead-list'),
    path('ai-recommendations/', AIRecommendationView.as_view(), name='ai-recommendations'),
]
