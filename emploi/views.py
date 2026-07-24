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

    # Quand on clique sur Enregistrer ou Modifier
    if request.method == "POST":

        # On récupère l'id envoyé par le formulaire Modifier
        idprof = request.POST.get("idprof")


        # ==========================
        # MODIFICATION D'UN PROF
        # ==========================

        if idprof:

            prof = get_object_or_404(
                Prof,
                idprof=idprof
            )

            form = ProfForm(
                request.POST,
                instance=prof
            )


        # ==========================
        # AJOUT D'UN PROF
        # ==========================

        else:

            form = ProfForm(
                request.POST
            )


        # Vérification du formulaire

        if form.is_valid():

            form.save()

            return redirect("prof")



    # Quand on ouvre la page
    else:

        form = ProfForm()



    # Récupération de tous les professeurs

    professeurs = Prof.objects.all()



    context = {

        "professeurs": professeurs,

        "form": form

    }



    return render(
        request,
        "professeur/prof.html",
        context
    )

def salle(request):
    return render(request , "salle/salle.html")

def emploi(request):
    return render(request , "emploi/emploi.html")

def classe(request):
    return render(request , "classe/classe.html")