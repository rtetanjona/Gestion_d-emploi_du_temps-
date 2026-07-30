from django.urls import path
from .import views
urlpatterns = [
    # DASHBORD
    path('dashboard/',views.dashboard, name="dashboard"),


    # CLASSE
    path('classe/', views.classe, name="classe" ),


    # EMPLOI
    path('emploi/', views.emploi, name="emploi"),
    

    # PROF
    path('prof/', views.list_prof, name="prof"),
    path("prof/ajouter/", views.ajoute_prof, name="ajoute_prof"),
    path("prof/modifier/<int:idprof>/", views.modifier_prof, name="modifier_prof"),
    path('prof/suprimer/<int:idprof>/', views.suprime_prof , name='suprime_prof'),


    # SALLE
    path('salle/', views.salle, name="salle")
]
