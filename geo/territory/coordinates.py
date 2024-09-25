from django.contrib.gis.geos import Point, LinearRing, Polygon


class CoordinatePoint:
    """Class for """

    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}"


class RingCoordinates:
    """
    Convert coordinates to Point and Polygon (django.contrib.gis.geos)
    Calculate (and rewrite) coordinates for possible antimeridian intersection,
    Define antimeridian intersection, rewrite coordinate if antimeridian intersection exists

    """
    # ring coordinates create using 4 points
    POINT_COUNT = 4

    def __init__(self, point_1, point_2, point_3, point_4):
        self._coordinates : [CoordinatePoint] = [point_1, point_2, point_3, point_4]
        self._antimeridian_intersection = self._is_antimeridian()
        if self._antimeridian_intersection:
            self.change_coordinates_for_antimeridian()

    @property
    def antimeridian_intersection(self) -> bool:
        """Ring (point1, point2, point3) contains antimeridian"""
        return self._antimeridian_intersection

    @property
    def geo_points(self) -> list[Point]:
        """Coordinate points as geo points (django.contrib.gis.geos.Point)"""
        geo_points = []
        for coordinate_point in self._coordinates:
            geo_points.append(Point(coordinate_point.latitude, coordinate_point.longitude))
        return geo_points

    @property
    def polygon(self):
        """Polygon (django.contrib.gis.geos.Polygon) from coordinates"""
        linear_ring = LinearRing(*self.geo_points)
        polygon = Polygon(linear_ring)
        return polygon

    @classmethod
    def create_from_coordinate_lists(cls, *coordinates: [float, float]):
        """Create class instance from list of point coordinates"""
        if len(coordinates) != cls.POINT_COUNT:
            raise WrongPointException(f"Count of coordinates must be {cls.POINT_COUNT}")
        if coordinates[0] != coordinates[-1]:
            raise WrongPointException(f"First and last coordinate point must be equal")
        points = []
        for num, coordinate in enumerate(coordinates):
            latitude = coordinate[0]
            longitude = coordinate[1]
            points.append(CoordinatePoint(latitude, longitude))
        return cls(*points)

    def _is_antimeridian(self):
        """
        Define if ring intersections antimeridian
        Return True if intersection exists or False if not
        """
        eastern_hemisphere = False
        western_hemisphere = False
        for point in self._coordinates:
            if point.longitude <= 180:
                eastern_hemisphere = True
            else:
                western_hemisphere = True
            if eastern_hemisphere and western_hemisphere:
                return True
        return False

    def change_coordinates_for_antimeridian(self):
        """
        Make change to coordinates due to antimeridian.
        Use this for antimeridian intersection polygon coordinate point.
        longitude = longitude -360 for every point if longitude more than 180.
        """
        for num, point in enumerate(self._coordinates):
            latitude = point.latitude
            longitude = point.longitude
            if longitude > 180:
                self._coordinates[num] = CoordinatePoint(latitude, longitude - 360)
            else:
                self._coordinates[num] = CoordinatePoint(latitude, longitude)

    def __repr__(self):
        return f"coordinates: {self._coordinates}, antimeridian: {self._antimeridian_intersection}"


class WrongPointException(Exception):
    """Wrong points """


if __name__ == '__main__':
    ring_coordinates = RingCoordinates(
        CoordinatePoint(1, 2),
        CoordinatePoint(10, 20),
        CoordinatePoint(30, 25),
        CoordinatePoint(1, 2)
    )
    ring_coordinates_from_coordinates = RingCoordinates.create_from_coordinate_lists([1, 2], [10, 20], [30, 25],[1, 2])
    print(ring_coordinates)
    print(ring_coordinates_from_coordinates)
