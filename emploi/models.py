
import datetime

from django.db import models



class Prof  (models.Model):

    GRADE_CHOICES = [
        ("PT", "Professeur Titulaire"),
        ("MC", "Maître de Conférences"),
        ("AESR", "Assistant d'Enseignement Supérieur et de Recherche"),
        ("HDR", "Docteur HDR"),
        ("DI", "Docteur en Informatique"),
        ("DOC", "Doctorant en Informatique"),
    ]

    idprof = models.AutoField(primary_key=True)
    nomprof = models.CharField(max_length=100)
    prenomprof = models.CharField(max_length=100)
    grad = models.CharField(
        max_length=10,
        choices=GRADE_CHOICES
    )

    def __str__(self):
        return f"{self.nomprof} {self.prenomprof}"


class Salle(models.Model):

    OCCUPATION_CHOICES = [
        ("Libre", "Libre"),
        ("Occupee", "Occupée"),
    ]

    idsalle = models.AutoField(primary_key=True)
    design = models.CharField(max_length=100)
    occupation = models.CharField(
        max_length=10,
        choices=OCCUPATION_CHOICES
    )

    def __str__(self):
        return self.design


class Classe(models.Model):

    idclass = models.AutoField(primary_key=True)
    niveau = models.CharField(max_length=100)

    def __str__(self):
        return self.niveau


class EmploiDuTemps(models.Model):

    DUREE_CHOICES = [
        (60, "1h"),
        (90, "1h30"),
        (120, "2h"),
        (180, "3h"),
        (240, "4h"),
    ]

    idsalle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE
    )

    idprof = models.ForeignKey(
        Prof,
        on_delete=models.CASCADE
    )

    idclass = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE
    )

    cours = models.CharField(max_length=100)

    date = models.DateTimeField()

    duree_minutes = models.PositiveIntegerField(
        choices=DUREE_CHOICES,
        default=90
    )

    @property
    def heure_fin(self):
        return self.date + datetime.timedelta(minutes=self.duree_minutes)

    def __str__(self):
        return self.cours