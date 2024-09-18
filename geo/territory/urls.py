from django.urls import path

from . import views, drf_views

urlpatterns = [
    path("", views.index, name="polygon"),
    path("polygons/", views.polygon_list, name="polygons"),
    path("form/", views.polygon_form, name="polygon_form"),

    path('polygon-list/', drf_views.PolygonList.as_view(), name='polygon-list'),
    path('polygon/<int:pk>/', drf_views.PolygonDetail.as_view(), name='polygon-detail'),
]
