from django.urls import path
from .views import ClientFollowUpView

app_name = 'clients'

urlpatterns = [
    path('follow-up/', ClientFollowUpView.as_view(), name='client-follow-up'),
]
