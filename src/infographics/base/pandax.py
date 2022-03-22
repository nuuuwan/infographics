from shapely.geometry import MultiPolygon, Polygon

from infographics.base import ds, shapely


def get_shapely_polygon_list_from_shape(shape):
    if isinstance(shape, MultiPolygon):
        return shapely.get_shapely_polygon_list_from_multipolygon(shape)
    if isinstance(shape, Polygon):
        return [shape]
    raise Exception('Unknown shape: ', type(shape))


def get_multipolygon_from_shapely_polygon_list(shapely_polygon_list):
    point_list_list = list(map(
        shapely.get_point_list_from_shapely_polygon_to,
        shapely_polygon_list,
    ))

    multipolygon = list(map(
        lambda point_list: list(map(
            shapely.get_xy_from_shapely_point,
            point_list,
        )),
        point_list_list,
    ))

    return multipolygon


def get_geodata_index(df):
    geodata_index = {}
    for row in df.itertuples():
        d = dict(row._asdict())

        shapely_polygon_list = get_shapely_polygon_list_from_shape(d['geometry'])
        multipolygon = get_multipolygon_from_shapely_polygon_list(
            shapely_polygon_list,
        )

        del d['geometry']
        geodata_index[d['id']] = d | {
            'multipolygon': multipolygon,
        }

    return ds.sort_dict_by_key(geodata_index)
