from django.shortcuts import render , redirect , get_object_or_404

from .models import Prof , Salle , EmploiDuTemps , Classe

from .forms import(
    ProfForms,
    SalleForms,
    ClasseForms,
    EmploiDuTempsForms
)

#  -------DASHBORD----------

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
        
        "profs": Prof.objects.all(),
        "salles": Salle.objects.all(),
        "classes": Classe.objects.all(),
        "emplois": EmploiDuTemps.objects.select_related(
            "idprof",
            "idsalle",
            "idclass"
        )
    }

    return render(request, "dashboard/dashboard.html", context)

# ------------PROF------------

def list_prof(request):
    profs = Prof.objects.all()
    form = ProfForms()
    return render(request, "professeur/prof.html", {'profs':profs , 'form':form})

def ajoute_prof(request):
    form = ProfForms(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('prof')
    return render(request , "professeur/prof.html" , {"form":form}) 

def modifier_prof(request, idprof):
    prof = get_object_or_404(Prof, idprof=idprof)

    if request.method == "POST":
        prof.nomprof = request.POST.get("nomprof")
        prof.prenomprof = request.POST.get("prenomprof")
        prof.grad = request.POST.get("grad")

        prof.save()

        return redirect("prof")

    return redirect("prof")

def suprime_prof(request , idprof):
    prof = get_object_or_404(Prof , idprof=idprof)
    if request.method =="POST":
        prof.delete()
        return redirect('prof')

    
# -----------SALLE---------------

def list_salle(request):
    salles =Salle.objects.all()
    form =  SalleForms()
    return render(request , "salle/salle.html" , {'salles':salles , 'form' : form})

# ----------EMPLOI------------

def emploi(request):
    return render(request , "emploi/emploi.html")


# -------------CLASSE---------------

def classe(request):
    return render(request , "classe/classe.html")