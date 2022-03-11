from shapely.geometry import MultiPolygon, Polygon
from utils import ds


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


def df_to_latlng_list_list(df):
    latlng_list_list_list = []
    for row in df.itertuples():
        shape = row.geometry
        if isinstance(shape, MultiPolygon):
            polygon_list = multipolygon_to_polygon_list(shape)
        elif isinstance(shape, Polygon):
            polygon_list = [shape]
        else:
            polygon_list = []

        point_list_list = list(map(
            polygon_to_point_list,
            polygon_list,
        ))

        latlng_list_list = list(map(
            lambda point_list: list(map(
                point_to_latlng,
                point_list,
            )),
            point_list_list,
        ))
        latlng_list_list_list.append(latlng_list_list)
    return latlng_list_list_list


def norm_latlng_list_list_list(
    latlng_list_list_list,
    map_r=0.8,
    size=(
        1600,
        900)):
    latlng_list = ds.flatten(ds.flatten(latlng_list_list_list))
    ((min_lat, min_lng), (max_lat, max_lng)) = get_bounds(latlng_list)
    lat_span = max_lat - min_lat
    lng_span = max_lng - min_lng

    r = lat_span / lng_span * (size[0] / size[1])
    padding_x = 0
    padding_y = 0
    if r > 1:
        padding_x = (1 - (1 / r)) / 2
    else:
        padding_y = (1 - r) / 2

    def t(latlng):
        lat, lng = latlng
        qy = (lat - min_lat) / lat_span
        qx = (lng - min_lng) / lng_span

        rx = padding_x + qx * (1 - padding_x * 2)
        ry = padding_y + qy * (1 - padding_y * 2)

        px = (rx * 2 - 1) * map_r
        py = (ry * 2 - 1) * map_r
        return (px, py)

    return list(map(
        lambda latlng_list_list: list(map(
            lambda latlng_list: list(map(
                t,
                latlng_list,
            )), latlng_list_list
        )),
        latlng_list_list_list,
    ))
