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
