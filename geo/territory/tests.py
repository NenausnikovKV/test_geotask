import io

from django.contrib.gis.geos import Polygon, Point, LinearRing
from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser

from .coordinates import RingCoordinates, CoordinatePoint
from .models import PolygonModel


class TestRingCoordinate(TestCase):

    def test_get_polygon_by_points(self):
        point_1 = CoordinatePoint(10, 10)
        point_2 = CoordinatePoint(12, 15)
        point_3 = CoordinatePoint(123, 198)
        point_4 = CoordinatePoint(10, 10)
        ring_coordinate = RingCoordinates(point_1, point_2, point_3, point_4)
        self.assertTrue(ring_coordinate.antimeridian_intersection)
        self.assertIn(Point(10, 10), ring_coordinate.geo_points)


class PolygonTests(TestCase):

    def test_create(self):
        point_1 = Point(10, 10)
        point_2 = Point(12, 15)
        point_3 = Point(123, 150)
        point_4 = Point(10, 10)
        linear_ring = LinearRing(point_1, point_2, point_3, point_4)
        test_polygon = Polygon(linear_ring)
        polygon_model = PolygonModel(
            name="test name",
            polygon = test_polygon,
            coordinate_line = "test coordinate line",
            antimeridian = True
        )
        polygon_model.save()
        db_polygon = PolygonModel.objects.filter(name="test name").first()
        self.assertEqual(polygon_model.coordinate_line, db_polygon.coordinate_line)

    def test_forms(self):
        name = 'something'
        coordinates = [[10, 10], [12, 15], [123, 198], [10, 10]]
        {"name": "wqer", "coordinates": [[10, 12], [15, 51], [65, 189], [10, 12]]}
        form_body = {"polygon_data": f'{{"name": "{name}", "coordinates": {coordinates}}}'}
        response = self.client.post(reverse("polygon_form"), form_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(PolygonModel.objects.filter(name=name).first().name, name)

    def test_root_page(self):
        address = reverse("polygon")
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)


class PolygonDRFTest(TestCase):

    def test_get_polygon_list(self):
        big_id = 10264
        name = "test polygon name"
        coordinates = [[10, 10], [12, 15], [123, 198], [10, 10]]
        data = {
            "id": big_id,
            "name": name,
            "coordinate_line": str(coordinates),
        }
        PolygonModel.objects.create(**data)
        address = reverse("polygon-list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertIn("id", response_data[0])
        self.assertIn("name", response_data[0])

    def test_create_polygon(self):
        address = reverse("polygon-list")
        name = "test polygon name"
        big_id = 10356
        coordinates = [[10, 10], [12, 15], [123, 198], [10, 10]]
        post_data = {
            "id": big_id,
            "name": name,
            "coordinates": coordinates,
        }
        response = self.client.post(address, data=post_data, content_type="application/json")
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = PolygonModel.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        PolygonModel.objects.filter(id=response_id).delete()
        self.assertFalse(get_by_response_id_queryset.exists())

        with self.assertRaises(PolygonModel.DoesNotExist):
            wrong_id = 99999999
            _ = PolygonModel.objects.get(id=wrong_id)

    def test_get_polygon_detail(self):
        big_id = 10265
        data = {
            "id": big_id,
            "name": "f = 7+9",
            "coordinate_line": "4 5 6",
        }
        PolygonModel.objects.create(**data)
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertIn("name", response_data)
        self.assertIn("id", response_data)
        self.assertIn("coordinate_line", response_data)

    def test_put_polygon(self):
        big_id = 10266
        data = {
            "id": big_id,
            "name": "start code",
            "coordinate_line": "4 5 7"
        }

        PolygonModel.objects.create(**data)
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        new_name = "new name"
        new_is_correct = True
        put_data = {
            "id": big_id,
            "name": new_name,
            "coordinate_line": "14 2 3"
        }
        response = self.client.put(address, data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = PolygonModel.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        self.assertEqual(response_data["name"], new_name)
        PolygonModel.objects.filter(id=big_id).delete()

    def test_delete_polygon(self):
        """        """
        big_id = 10267
        data = {
            "id": big_id,
            "name": "start code",
            "coordinate_line": "sdfasf"
        }
        with transaction.atomic():
            PolygonModel.objects.create(**data)
        big_id_queryset = PolygonModel.objects.filter(id=big_id)
        self.assertTrue(big_id_queryset.exists())
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        response = self.client.delete(address)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(big_id_queryset.exists())
        with self.assertRaises(PolygonModel.DoesNotExist):
            wrong_id = big_id
            _ = PolygonModel.objects.get(id=wrong_id)
