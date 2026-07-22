from django.shortcuts import render , redirect , get_object_or_404

from .models import Prof , Salle , EmploiDuTemps , Classe

from .forms import(
    ProfForm,
    SalleFroms,
    ClasseFrom,
    EmploiDuTempsFroms
)

def dashboard(request):
    nombre_prof = Prof.objects.count()
    nombre_salle = Salle.objects.count()
    nombre_classe = Classe.objects.count()
    nombre_emploi = EmploiDuTemps.objects.count()

    context = {
        "nombre_prof": nombre_prof,
        "nombre_salle": nombre_salle,
        "nombre_classe": nombre_classe,
        "nombre_emploi": nombre_emploi,
    }

    return render(request, "dashboard/dashboard.html", context)

def prof(request):

    if request.method == "POST":
        form = ProfForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("prof")

    else:
        form = ProfForm()

    professeurs = Prof.objects.all()

    context = {
        "professeurs": professeurs,
        "form": form
    }

    return render(request, "professeur/prof.html", context)


def salle(request):
    return render(request , "salle/salle.html")

def emploi(request):
    return render(request , "emploi/emploi.html")

def classe(request):
    return render(request , "classe/classe.html")