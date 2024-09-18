from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Polygon
from .serializers import PolygonSerializer


class PolygonList(APIView):
    """
    List all polygons, or create a new polygon.
    """
    def get(self, request, format=None):
        polygons = Polygon.objects.all()
        serializer = PolygonSerializer(polygons, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PolygonSerializer(data=request.data, context={"request": request})
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
            return Polygon.objects.get(pk=pk)
        except Polygon.DoesNotExist:
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
