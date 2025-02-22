from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.conf.urls.i18n import i18n_patterns

app_name = 'home'

urlpatterns = i18n_patterns(
    path('', cache_page(60 * 15)(TemplateView.as_view(template_name="home/index.html")), name='home'),
    prefix_default_language=False
)
