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
            'date'
        ]
