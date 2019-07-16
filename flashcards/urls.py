"""flashcards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from core import views as core_views
from core import json_views

urlpatterns = [
    path('', RedirectView.as_view(url='/stacks/')),
    path('stacks/', core_views.StackListView.as_view(), name='stack-list'),
    path('stacks/<int:pk>/',
         core_views.StackDetailView.as_view(),
         name='stack-detail'),
    path('stacks/<int:stack_pk>/create_card/',
         core_views.card_create,
         name='card-create'),
    path('stacks/<int:stack_pk>/cards/',
         core_views.stack_all_cards,
         name='stack-all-cards'),
    path('stacks/<int:stack_pk>/quiz/',
         core_views.stack_quiz,
         name='stack-quiz'),
    path('card-results/<int:card_pk>/',
         core_views.card_results,
         name='card-results'),
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.simple.urls')),
    path('json/stacks/<int:stack_pk>/random-card/',
         json_views.random_card,
         name="json_random_card"),
    path('json/card-results/<int:card_pk>/',
         json_views.post_card_results,
         name="json_post_card_results"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
