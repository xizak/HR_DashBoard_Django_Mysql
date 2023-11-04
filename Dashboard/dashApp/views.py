from django.shortcuts import render
from .indicators import *
from django.utils.safestring import mark_safe
import json


def convert_to_json(data):
    data_dict = dict(data)
    json_str = json.dumps(data_dict)
    return json_str

def landing_view(request):
    context = {
        "effectif": calculer_effectif_total(),
        "genre": mark_safe(json.dumps(dict(repartition_par_genre()))),
        "departement": mark_safe(json.dumps(dict(repartition_par_departement()))),
        "age": mark_safe(json.dumps(dict(repartition_par_age()))),
        "genreRadar": mark_safe(json.dumps(distribution_par_genre_par_departement())),
        "genreHeatMap": mark_safe(json.dumps(repartition_par_age_departement())),


    }
    return render(request, "dashApp/landing.html", context=context)

