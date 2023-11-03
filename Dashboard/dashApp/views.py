from django.shortcuts import render
from .indicators import *


def landing_view(request):
    context = {
        "effectif": calculer_effectif_total(),
        "genre": dict(repartition_par_genre()),
        }
    return render(request, "dashApp/landing.html", context=context)
