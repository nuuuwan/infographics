def get_shapely_polygon_list_from_multipolygon(multipolygon):
    return list(multipolygon)


def get_shapely_point_list_from_polygon(polygon):
    return list(polygon.exterior.coords)


def get_xy_from_shapely_point(point):
    return (point[1], point[0])
