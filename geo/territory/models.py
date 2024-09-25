from django.contrib.gis.db import models as gis_models
# from django.contrib.gis.geos import Point, LineString


class PolygonModel(gis_models.Model):
    name = gis_models.CharField(max_length=120, default="Неизвестный полигон")
    polygon = gis_models.PolygonField(null=True)
    coordinate_line = gis_models.CharField(max_length=200, null=True)
    antimeridian = gis_models.BooleanField(null=True)

    def __str__(self):
        return self.name
