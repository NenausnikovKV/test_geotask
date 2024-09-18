from django.contrib.gis.db import models as gis_models
from django.contrib.gis.gdal.geometries import Polygon
from django.db import models


class Polygon(models.Model):
    name = models.CharField(max_length=120)
    # polygon = gis_models.PolygonField(default=Polygon(((0, 0), (0, 1), (1, 1), (1, 0), (0, 0)), ((0.4, 0.4), (0.4, 0.6), (0.6, 0.6), (0.6, 0.4), (0.4, 0.4))))
    polygon = gis_models.PolygonField()

    def __str__(self):
        return self.name
