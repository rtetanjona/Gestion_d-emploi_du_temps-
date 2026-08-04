import datetime

from django import forms
from .models import Prof, Salle, Classe, EmploiDuTemps

class ProfForms(forms.ModelForm):
    class Meta:
        model = Prof
        fields = ['nomprof','prenomprof','grad']

     
class SalleForms(forms.ModelForm):
    class Meta:
        model = Salle
        fields = ['design', "occupation"]

class ClasseForms(forms.ModelForm):
    class Meta:
        model = Classe
        fields = [ 'niveau']

class EmploiDuTempsForms(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = [
            'idsalle',
            'idprof',
            'idclass',
            'cours',
            'date',
            'duree_minutes'
        ]
        widgets = {
            'date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'input input-bordered w-full'},
                format='%Y-%m-%dT%H:%M',
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        duree = cleaned_data.get('duree_minutes')

        if not (date and duree):
            return cleaned_data

        fin = date + datetime.timedelta(minutes=duree)

        def chevauche(seance):
            return seance.date < fin and seance.heure_fin > date

        champs_a_verifier = [
            ('idsalle', cleaned_data.get('idsalle'), "La salle {} est déjà réservée de {} à {}."),
            ('idprof', cleaned_data.get('idprof'), "Le professeur {} a déjà cours de {} à {}."),
            ('idclass', cleaned_data.get('idclass'), "La classe {} a déjà cours de {} à {}."),
        ]

        for champ, valeur, message in champs_a_verifier:
            if not valeur:
                continue
            existantes = EmploiDuTemps.objects.filter(**{champ: valeur}).exclude(pk=self.instance.pk)
            for seance in existantes:
                if chevauche(seance):
                    self.add_error(champ, message.format(
                        valeur,
                        seance.date.strftime('%d/%m/%Y %H:%M'),
                        seance.heure_fin.strftime('%H:%M'),
                    ))
                    break

        return cleaned_data
