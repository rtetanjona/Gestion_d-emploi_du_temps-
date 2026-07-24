from django import forms
from .models import Prof, Salle, Classe, EmploiDuTemps

class ProfForm(forms.ModelForm):
    class Meta:
        model = Prof
        fields = "__all__"

        # Définition des styles pour chaque champ
        widgets = {
            'nomprof': forms.TextInput(attrs={
                'class': 'input input-bordered input-lg input-primary rounded-full w-full', 
                'placeholder': 'Entrez le nom',
                'required': True # Force l'attribut HTML5 'required'
            }),
            'prenomprof': forms.TextInput(attrs={
                'class': 'input input-bordered input-lg input-primary rounded-full w-full', 
                'placeholder': 'Entrez le prénom',
                'required': True
            }),
            # Le grade reste en taille normale pour le contraste, ou change 'select' en 'select-lg'
            'grad': forms.Select(attrs={
                'class': 'select select-bordered rounded-full w-full'
            }),
        }

class SalleFroms(forms.ModelForm):
    class Meta:
        model = Salle
        fields = "__all__"

class ClasseFrom(forms.ModelForm):
    class Meta:
        model = Classe
        fields = "__all__"

class EmploiDuTempsFroms(forms.ModelForm):
    class Meta:
        model = EmploiDuTemps
        fields = "__all__"
