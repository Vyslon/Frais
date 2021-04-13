from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView

urlpatterns = [
    path('login/', views.MyLoginView.as_view()),
    path('', RedirectView.as_view(url='fiches-frais/', permanent=True)),
    path('fiches-frais/', login_required(views.fiches_frais), name='les-fiches'),
    path('fiches-frais/nouvelle-fiche/', login_required(views.FicheFraisCreate.as_view()), name='nouvelle-fiche-frais'),
    path('fiches-frais/<str:mois>/saisie-frais-hors-forfait/', login_required(views.LigneFraisHorsForfaitCreate.as_view()), name='saisie-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/edition-frais-forfaitaire/<int:pk>/', login_required(views.LigneFraisForfaitUpdate.as_view()), name='edit-ligne-forfait'),
    path('fiches-frais/<str:mois>/edition-frais-hors-forfait/<int:pk>/', login_required(views.LigneFraisHorsForfaitUpdate.as_view()), name='edit-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/suppression-frais-hors-forfait/<int:pk>/', login_required(views.LigneFraisHorsForfaitDelete.as_view()), name='suppr-ligne-hors-forfait'),
    path('fiches-frais/<str:mois>/pdf/', login_required(views.une_fiche_frais_pdf), name='une-fiche-pdf'),
    path('fiches-frais/<str:mois>/', login_required(views.une_fiche_frais), name='une-fiche'),
]
