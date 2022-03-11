def get_bounds(latlng_list):
    min_lat, min_lng = 180, 180
    max_lat, max_lng = -180, -180
    for lat, lng in latlng_list:
        min_lat = min(min_lat, lat)
        min_lng = min(min_lng, lng)
        max_lat = max(max_lat, lat)
        max_lng = max(max_lng, lng)
    return ((min_lat, min_lng), (max_lat, max_lng))
def multipolygon_to_polygon_list(multipolygon):
    return list(multipolygon)


def polygon_to_point_list(polygon):
    return list(polygon.exterior.coords)


def point_to_latlng(point):
    return (point[1], point[0])
