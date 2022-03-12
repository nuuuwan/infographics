"""
Various latlng related utils.

point hierarchy
0 - coordinates (x or y, lat or lng)
1 - point
2 - polygon (point_list)
3 - multipolygon (point_list_list)
"""
from shapely.geometry import MultiPolygon, Polygon
from utils import ds


def get_bounds(polygon):
    min_lat, min_lng = 180, 180
    max_lat, max_lng = -180, -180
    for lat, lng in polygon:
        min_lat = min(min_lat, lat)
        min_lng = min(min_lng, lng)
        max_lat = max(max_lat, lat)
        max_lng = max(max_lng, lng)
    return ((min_lat, min_lng), (max_lat, max_lng))


def get_midlatlng(multipolygon):
    polygon = ds.flatten(multipolygon)
    ((min_lat, min_lng), (max_lat, max_lng)) = get_bounds(polygon)
    mid_lat = (min_lat + max_lat) / 2
    mid_lng = (min_lng + max_lng) / 2
    return (mid_lat, mid_lng)


def shapely_multipolygon_to_polygon_list(multipolygon):
    return list(multipolygon)


def shapely_polygon_to_point_list(polygon):
    return list(polygon.exterior.coords)


def shapely_point_to_latlng(point):
    return (point[1], point[0])


def df_to_geodata_list(df):
    geodata_list = []
    for row in df.itertuples():
        d = dict(row._asdict())

        shape = d['geometry']
        if isinstance(shape, MultiPolygon):
            polygon_list = shapely_multipolygon_to_polygon_list(shape)
        elif isinstance(shape, Polygon):
            polygon_list = [shape]
        else:
            polygon_list = []

        point_list_list = list(map(
            shapely_polygon_to_point_list,
            polygon_list,
        ))

        multipolygon = list(map(
            lambda point_list: list(map(
                shapely_point_to_latlng,
                point_list,
            )),
            point_list_list,
        ))

        del d['geometry']
        geodata_list.append(d | {
            'multipolygon': multipolygon,
        })
    return geodata_list


def norm_multi2polygon(
    multi2polygon,
    map_r=0.8,
    size=(
        1600,
        900)):
    polygon = ds.flatten(ds.flatten(multi2polygon))
    ((min_lat, min_lng), (max_lat, max_lng)) = get_bounds(polygon)
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
        lambda multipolygon: list(map(
            lambda polygon: list(map(
                t,
                polygon,
            )), multipolygon
        )),
        multi2polygon,
    ))
