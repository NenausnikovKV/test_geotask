from rest_framework import serializers

from .models import PolygonModel


class PolygonSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="polygon-detail")

    class Meta:
        model = PolygonModel
        fields = ['url', 'id', 'name', "polygon", "coordinate_line", "antimeridian"]
