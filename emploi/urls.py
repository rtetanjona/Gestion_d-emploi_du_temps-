from django.contrib.auth.decorators import login_required
from django.urls import path
from .import views

urlpatterns = [
    # DASHBORD
    path('dashboard/', login_required(views.dashboard), name="dashboard"),


    # CLASSE
    path('classe/', login_required(views.classe), name="classe" ),
    path('classe/ajouter/', login_required(views.ajoute_classe), name="ajoute_classe"),
    path('classe/modifier/<int:idclass>/', login_required(views.modifier_classe), name="modifier_classe"),
    path('classe/suprimer/<int:idclass>/', login_required(views.suprime_classe), name="suprime_classe"),
    path('classe/<int:idclass>/emploi/', login_required(views.emploi_classe), name="emploi_classe"),
    path('classe/<int:idclass>/emploi/pdf/', login_required(views.emploi_classe_pdf), name="emploi_classe_pdf"),


    # EMPLOI
    path('emploi/', login_required(views.emploi), name="emploi"),
    path('emploi/ajouter/', login_required(views.ajoute_emploi), name="ajoute_emploi"),
    path('emploi/modifier/<int:id>/', login_required(views.modifier_emploi), name="modifier_emploi"),
    path('emploi/supprimer/<int:id>/', login_required(views.suprime_emploi), name="suprime_emploi"),


    # PROF
    path('prof/', login_required(views.list_prof), name="prof"),
    path("prof/ajouter/", login_required(views.ajoute_prof), name="ajoute_prof"),
    path("prof/modifier/<int:idprof>/", login_required(views.modifier_prof), name="modifier_prof"),
    path('prof/suprimer/<int:idprof>/', login_required(views.suprime_prof) , name='suprime_prof'),


    # SALLE
    path('salle/', login_required(views.list_salle), name="salle"),
    path("salle/ajouter/", login_required(views.ajoute_salle), name="ajoute_salle"),
    path("salle/modifier/<int:idsalle>/", login_required(views.modifier_salle), name="modifier_salle"),
    path("salle/suprimer/<int:idsalle>/", login_required(views.suprime_salle), name="suprime_salle"),


]
