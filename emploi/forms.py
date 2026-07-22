from django import forms
from .models import Prof, Salle, Classe, EmploiDuTemps

class ProfForm(forms.ModelForm):
    class Meta:
        model = Prof
        fields = "__all__"

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
