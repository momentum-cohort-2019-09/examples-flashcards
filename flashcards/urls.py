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
from django.urls import path
from django.views.generic import RedirectView
from core import views as core_views

urlpatterns = [
    path('', RedirectView.as_view(url='/stacks/')),
    path('stacks/', core_views.stack_list, name='stack-list'),
    path('stacks/<int:stack_pk>/', core_views.stack_detail,
         name='stack-detail'),
    path('stacks/<int:stack_pk>/create_card/',
         core_views.card_create,
         name='card-create'),
    path('stacks/<int:stack_pk>/quiz/',
         core_views.stack_quiz,
         name='stack-quiz'),
    path('card-results/<int:card_pk>/',
         core_views.card_results,
         name='card-results'),
    path('admin/', admin.site.urls),
]
