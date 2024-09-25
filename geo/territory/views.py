import json

from django.http import Http404
from django.shortcuts import render

from .coordinates import RingCoordinates
from .models import PolygonModel, POLYGON_DEFAULT_NAME


def index(request):
    """Territory page list"""
    return render(request, "territory/index.html")


def polygon_list(request):
    """Template polygon list"""
    try:
        polygons = PolygonModel.objects.all()
        context = {"polygon_list": polygons}
    except Exception:
        raise Http404("Polygon does not exist")
    else:
        return render(request, "territory/polygon_list.html", context)


def polygon_form(request):
    """Polygon form"""
    if request.method == "POST":
        try:
            polygon_data_json = request.POST.get("polygon_data")
            polygon_data = json.loads(polygon_data_json)
            polygon_name = polygon_data.get("name")
            if not polygon_name:
                polygon_name = POLYGON_DEFAULT_NAME
            polygon_coordinates = polygon_data.get("coordinates")
            ring_coordinates = RingCoordinates.create_from_coordinate_lists(*polygon_coordinates)

            PolygonModel.objects.create(
                name=polygon_name,
                polygon=ring_coordinates.polygon,
                coordinate_line=polygon_coordinates,
                antimeridian=ring_coordinates.antimeridian_intersection
            )
        except Exception as e:
            raise Http404("Wrong polygon data")
    http_response = render(request, template_name="territory/polygon_form.html")
    return http_response
