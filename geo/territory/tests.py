import io

from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework.parsers import JSONParser

from .models import Polygon


# Create your tests here.

class PolygonTests(TestCase):

    def test_create(self):
        future_question = Polygon(name="any name")
        future_question.save()

    def test_forms(self):
        name = 'something'
        coordinates = "(0,1)"
        form_body = {'polygon_name': name, "polygon_coordinates": coordinates}
        response = self.client.post(reverse("polygon_form"), {'polygon_name': name})
        self.assertEqual(response.status_code, 200)
        assert Polygon.objects.filter(name=name).first().name == name

    def test_root_page(self):
        address = reverse("polygon")
        response = self.client.get(address)
        self.assertEqual(response.status_code, 200)


class PolygonDRFTest(TestCase):

    def test_get_polygon_list(self):
        big_id = 10264
        data = {
            "id": big_id,
            "name": "test polygon name",
            "coordinates": "123",
        }
        with transaction.atomic():
            Polygon.objects.create(**data)

        address = reverse("polygon-list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data[0])
        self.assertIn("name", response_data[0])

    def test_create_polygon(self):
        address = reverse("polygon-list")
        post_data = {
            "name": "test_name",
            "coordinates": "asdas",
        }

        response = self.client.post(address, data=post_data, content_type="application/json")
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = Polygon.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        Polygon.objects.filter(id=response_id).delete()
        self.assertFalse(get_by_response_id_queryset.exists())

        with self.assertRaises(Polygon.DoesNotExist):
            wrong_id = 99999999
            _ = Polygon.objects.get(id=wrong_id)

    def test_get_polygon_detail(self):
        big_id = 10265
        data = {
            "id": big_id,
            "name": "f = 7+9",
            "coordinates": "4 5 6",
        }

        Polygon.objects.create(**data)
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertIn("name", response_data)
        self.assertIn("id", response_data)
        self.assertIn("coordinates", response_data)

    def test_put_polygon(self):
        big_id = 10266
        data = {
            "id": big_id,
            "name": "start code",
            "coordinates": "4 5 7"
        }

        Polygon.objects.create(**data)
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        new_name = "new name"
        new_is_correct = True
        put_data = {
            "id": big_id,
            "name": new_name,
            "coordinates": "14 2 3"
        }
        response = self.client.put(address, data=put_data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = Polygon.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        self.assertEqual(response_data["name"], new_name)
        Polygon.objects.filter(id=big_id).delete()

    def test_delete_polygon(self):
        """        """
        big_id = 10267
        data = {
            "id": big_id,
            "name": "start code",
            "coordinates": "sdfasf"
        }
        with transaction.atomic():
            Polygon.objects.create(**data)
        big_id_queryset = Polygon.objects.filter(id=big_id)
        self.assertTrue(big_id_queryset.exists())
        address = reverse("polygon-detail", kwargs={"pk": big_id})
        response = self.client.delete(address)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(big_id_queryset.exists())
        with self.assertRaises(Polygon.DoesNotExist):
            wrong_id = big_id
            _ = Polygon.objects.get(id=wrong_id)
