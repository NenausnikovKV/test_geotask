from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Polygon
from django.db import models


class PolygonModel(models.Model):
    name = models.CharField(max_length=120)
    polygon = gis_models.PolygonField()
