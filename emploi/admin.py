from django.contrib import admin
from .models import *


@admin.register(Prof)
class ProfAdmin(admin.ModelAdmin):

    list_display = (
        "idprof",
        "nomprof",
        "prenomprof",
        "grad"
    )


@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):

    list_display = (
        "idsalle",
        "design",
        "occupation"
    )


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):

    list_display = (
        "idclass",
        "niveau"
    )


@admin.register(EmploiDuTemps)
class EmploiDuTempsAdmin(admin.ModelAdmin):

    list_display = (
        "cours",
        "idprof",
        "idclass",
        "idsalle",
        "date"
    )