from django.http import Http404
from django.shortcuts import render

from .models import Polygon


def index(request):
    return render(request, "territory/index.html")


def polygon_list(request):
    """Template polygon list"""
    try:
        polygons = Polygon.objects.all()
        context = {"polygon_list": polygons}
    except Exception:
        raise Http404("Polygon does not exist")
    else:
        return render(request, "territory/polygon_list.html", context)


def polygon_form(request):
    """Polygon form"""
    if request.method == "POST":
        polygon_name = request.POST.get("polygon_name")
        polygon_coordinates = request.POST.get("polygon_coordinates", "")
        Polygon.objects.create(name=polygon_name, coordinates=polygon_coordinates)
    http_response = render(request, template_name="territory/polygon_form.html")
    return http_response
