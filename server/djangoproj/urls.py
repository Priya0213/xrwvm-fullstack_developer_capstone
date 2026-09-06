"""djangoproj URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Django app API routes
    path('djangoapp/', include('djangoapp.urls')),

    # Home page
    path('', TemplateView.as_view(template_name="Home.html")),

    # About Us page
    path('about/', TemplateView.as_view(template_name="About.html")),

    # Contact Us page
    path('contact/', TemplateView.as_view(template_name="Contact.html")),

    # React Login page
    path('login/', TemplateView.as_view(template_name="index.html")),

    path('register/', TemplateView.as_view(template_name="index.html")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)