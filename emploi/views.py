import datetime

from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from .models import Prof , Salle , EmploiDuTemps , Classe

from .forms import(
    ProfForms,
    SalleForms,
    ClasseForms,
    EmploiDuTempsForms
)

# -------SEMAINE A GLANCE----------

JOURS_SEMAINE = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
HEURE_DEBUT_AXE = 7
HEURE_FIN_AXE = 19

PALETTE_COURS = [
    "bg-primary/20 text-primary border-primary",
    "bg-secondary/20 text-secondary border-secondary",
    "bg-accent/20 text-accent border-accent",
    "bg-info/20 text-info border-info",
    "bg-success/20 text-success border-success",
    "bg-warning/20 text-warning border-warning",
    "bg-error/20 text-error border-error",
]

def _flash_form_errors(request, form):
    for champ, erreurs in form.errors.items():
        for erreur in erreurs:
            messages.error(request, erreur)


def _semaine_a_glance(request, px_par_heure):
    semaine_param = request.GET.get('semaine')
    lundi = None
    if semaine_param:
        try:
            lundi = datetime.datetime.strptime(semaine_param, "%Y-%m-%d").date()
        except ValueError:
            lundi = None
    if lundi is None:
        aujourdhui = datetime.date.today()
        lundi = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())

    vendredi_fin = lundi + datetime.timedelta(days=5)
    hauteur_totale_semaine = (HEURE_FIN_AXE - HEURE_DEBUT_AXE) * px_par_heure

    jours = [
        {"nom": JOURS_SEMAINE[i], "date": lundi + datetime.timedelta(days=i), "evenements": []}
        for i in range(5)
    ]

    seances = EmploiDuTemps.objects.filter(
        date__date__gte=lundi,
        date__date__lt=vendredi_fin,
    ).select_related("idclass", "idprof", "idsalle")

    for s in seances:
        jour_index = (s.date.date() - lundi).days
        if jour_index < 0 or jour_index > 4:
            continue

        minutes_axe = (HEURE_FIN_AXE - HEURE_DEBUT_AXE) * 60

        minutes_depuis_debut = (s.date.hour - HEURE_DEBUT_AXE) * 60 + s.date.minute
        minutes_depuis_debut = max(0, min(minutes_depuis_debut, minutes_axe))
        top_px = minutes_depuis_debut * px_par_heure / 60

        minutes_fin = minutes_depuis_debut + s.duree_minutes
        minutes_fin = max(0, min(minutes_fin, minutes_axe))
        height_px = max(minutes_fin - minutes_depuis_debut, 10) * px_par_heure / 60

        couleur = PALETTE_COURS[sum(ord(c) for c in s.cours) % len(PALETTE_COURS)]

        jours[jour_index]["evenements"].append({
            "obj": s,
            "top_px": top_px,
            "height_px": height_px,
            "heure_label": s.date.strftime("%H:%M"),
            "heure_fin_label": s.heure_fin.strftime("%H:%M"),
            "couleur": couleur,
        })

    heures_axe = [
        {"label": f"{h}:00", "top_px": (h - HEURE_DEBUT_AXE) * px_par_heure}
        for h in range(HEURE_DEBUT_AXE, HEURE_FIN_AXE + 1)
    ]

    return {
        "jours": jours,
        "heures_axe": heures_axe,
        "hauteur_totale_semaine": hauteur_totale_semaine,
        "semaine_prec": (lundi - datetime.timedelta(days=7)).isoformat(),
        "semaine_suiv": (lundi + datetime.timedelta(days=7)).isoformat(),
    }

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
    context.update(_semaine_a_glance(request, px_par_heure=40))

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
    _flash_form_errors(request, form)
    return redirect('prof')

def modifier_prof(request, idprof):
    prof = get_object_or_404(Prof, idprof=idprof)
    form = ProfForms(request.POST or None, instance=prof)
    if form.is_valid():
        form.save()
        return redirect('prof')
    _flash_form_errors(request, form)
    return redirect('prof')

def suprime_prof(request , idprof):
    prof = get_object_or_404(Prof , idprof=idprof)
    if request.method =="POST":
        prof.delete()
        return redirect('prof')
    return redirect('prof')

# -----------SALLE---------------

def list_salle(request):
    salles = Salle.objects.all()
    form = SalleForms()

    date_recherche = request.GET.get('date_recherche')
    salles_libres = None
    if date_recherche:
        try:
            instant_recherche = timezone.make_aware(
                datetime.datetime.strptime(date_recherche, "%Y-%m-%dT%H:%M")
            )
        except ValueError:
            instant_recherche = None

        if instant_recherche:
            seances_du_jour = EmploiDuTemps.objects.filter(
                date__date=instant_recherche.date()
            )

            idsalle_occupees = [
                s.idsalle_id for s in seances_du_jour
                if s.date <= instant_recherche < s.heure_fin
            ]

            salles_libres = Salle.objects.exclude(idsalle__in=idsalle_occupees)

    return render(request, "salle/salle.html", {
        'salles': salles,
        'form': form,
        'date_recherche': date_recherche,
        'salles_libres': salles_libres,
    })

def ajoute_salle(request):
    form = SalleForms(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('salle')
    _flash_form_errors(request, form)
    return redirect('salle')

def modifier_salle(request, idsalle):
    salle = get_object_or_404(Salle, idsalle=idsalle)
    form = SalleForms(request.POST or None, instance=salle)
    if form.is_valid():
        form.save()
        return redirect('salle')
    _flash_form_errors(request, form)
    return redirect('salle')

def suprime_salle(request, idsalle):
    salle = get_object_or_404(Salle, idsalle=idsalle)
    if request.method == "POST":
        salle.delete()
        return redirect('salle')
    return redirect('salle')

# ----------EMPLOI------------

def emploi(request):
    emplois = EmploiDuTemps.objects.select_related(
        "idsalle", "idprof", "idclass"
    ).order_by("date")
    form = EmploiDuTempsForms()
    context = {
        "emplois": emplois,
        "form": form,
        "salles": Salle.objects.all(),
        "profs": Prof.objects.all(),
        "classes": Classe.objects.all(),
        "duree_choices": EmploiDuTemps.DUREE_CHOICES,
    }
    context.update(_semaine_a_glance(request, px_par_heure=60))
    return render(request, "emploi/emploi.html", context)

def ajoute_emploi(request):
    form = EmploiDuTempsForms(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('emploi')
    _flash_form_errors(request, form)
    return redirect('emploi')

def modifier_emploi(request, id):
    seance = get_object_or_404(EmploiDuTemps, id=id)
    form = EmploiDuTempsForms(request.POST or None, instance=seance)
    if form.is_valid():
        form.save()
        return redirect('emploi')
    _flash_form_errors(request, form)
    return redirect('emploi')

def suprime_emploi(request, id):
    seance = get_object_or_404(EmploiDuTemps, id=id)
    if request.method == "POST":
        seance.delete()
        return redirect('emploi')
    return redirect('emploi')

# -------------CLASSE---------------

def classe(request):
    classes = Classe.objects.all()
    form = ClasseForms()
    return render(request, "classe/classe.html", {"classes": classes, "form": form})

def ajoute_classe(request):
    form = ClasseForms(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('classe')
    _flash_form_errors(request, form)
    return redirect('classe')

def modifier_classe(request, idclass):
    classe_obj = get_object_or_404(Classe, idclass=idclass)
    form = ClasseForms(request.POST or None, instance=classe_obj)
    if form.is_valid():
        form.save()
        return redirect('classe')
    _flash_form_errors(request, form)
    return redirect('classe')

def suprime_classe(request, idclass):
    classe_obj = get_object_or_404(Classe, idclass=idclass)
    if request.method == "POST":
        classe_obj.delete()
        return redirect('classe')
    return redirect('classe')

def emploi_classe(request, idclass):
    classe_obj = get_object_or_404(Classe, idclass=idclass)
    seances = EmploiDuTemps.objects.filter(
        idclass=idclass
    ).select_related("idsalle", "idprof").order_by("date")
    return render(request, "classe/emploi_classe.html", {
        "classe_obj": classe_obj,
        "seances": seances,
    })

def emploi_classe_pdf(request, idclass):
    classe_obj = get_object_or_404(Classe, idclass=idclass)

    debut_str = request.GET.get('debut')
    debut = None
    if debut_str:
        try:
            debut = datetime.datetime.strptime(debut_str, "%Y-%m-%d").date()
        except ValueError:
            debut = None
    if debut is None:
        aujourdhui = datetime.date.today()
        debut = aujourdhui - datetime.timedelta(days=aujourdhui.weekday())

    fin = debut + datetime.timedelta(days=7)

    seances = EmploiDuTemps.objects.filter(
        idclass=idclass,
        date__date__gte=debut,
        date__date__lt=fin,
    ).select_related("idsalle", "idprof").order_by("date")

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="emploi_{classe_obj.niveau}_{debut}.pdf"'
    )

    doc = SimpleDocTemplate(response, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = [
        Paragraph(
            f"Emploi du temps - {classe_obj.niveau} - semaine du {debut.strftime('%d/%m/%Y')}",
            styles["Title"],
        ),
        Spacer(1, 1 * cm),
    ]

    data = [["Date", "Heure", "Cours", "Professeur", "Salle"]]
    for s in seances:
        data.append([
            s.date.strftime("%d/%m/%Y"),
            f"{s.date.strftime('%H:%M')} - {s.heure_fin.strftime('%H:%M')}",
            s.cours,
            str(s.idprof),
            str(s.idsalle),
        ])

    if len(data) == 1:
        elements.append(Paragraph("Aucune séance cette semaine.", styles["Normal"]))
    else:
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elements.append(table)

    doc.build(elements)
    return response