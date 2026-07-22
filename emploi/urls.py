from django.urls import path
from .import views
urlpatterns = [
    path('dashboard/',views.dashboard, name="dashboard"),
    path('classe/', views.classe, name="classe" ),
    path('emploi/', views.emploi, name="emploi"),
    path('prof/', views.prof, name="prof"),
    path('salle/', views.salle, name="salle")
]
