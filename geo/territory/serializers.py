from rest_framework import serializers

from .models import Polygon


class PolygonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="polygon-detail")

    class Meta:
        model = Polygon
        fields = ['url', 'id', 'name', "coordinates"]
