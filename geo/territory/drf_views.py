from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .coordinates import RingCoordinates
from .models import PolygonModel, POLYGON_DEFAULT_NAME
from .serializers import PolygonSerializer


class PolygonList(APIView):
    """
    List all polygons, or create a new polygon.
    """
    def get(self, request, format=None):
        polygons = PolygonModel.objects.all()
        serializer = PolygonSerializer(polygons, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        polygon_name = request.data.get("name")
        polygon_coordinates = request.data.get("coordinates")
        ring_coordinates = RingCoordinates.create_from_coordinate_lists(*polygon_coordinates)

        if not polygon_name:
            polygon_name = POLYGON_DEFAULT_NAME
        data = {
            "name": polygon_name,
            "polygon": ring_coordinates.polygon,
            "coordinate_line": str(polygon_coordinates),
            "antimeridian": ring_coordinates.antimeridian_intersection
        }
        serializer = PolygonSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PolygonDetail(APIView):
    """
    Retrieve, update or delete a polygon instance.
    """
    def get_object(self, pk):
        try:
            return PolygonModel.objects.get(pk=pk)
        except PolygonModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        polygon = self.get_object(pk)
        serializer = PolygonSerializer(polygon, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        polygon = self.get_object(pk)
        serializer = PolygonSerializer(polygon, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        polygon = self.get_object(pk)
        polygon.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
