from shapely.geometry import MultiPolygon, Polygon

from infographics.base import ds, shapely


def shape_to_shapely_polygon_list(shape):
    if isinstance(shape, MultiPolygon):
        return shapely.shapely_multipolygon_to_polygon_list(shape)
    if isinstance(shape, Polygon):
        return [shape]
    raise Exception('Unknown shape: ', type(shape))


def shapely_polygon_list_to_multipolygon(shapely_polygon_list):
    point_list_list = list(map(
        shapely.shapely_polygon_to_point_list,
        shapely_polygon_list,
    ))

    multipolygon = list(map(
        lambda point_list: list(map(
            shapely.shapely_point_to_xy,
            point_list,
        )),
        point_list_list,
    ))

    return multipolygon


def df_to_geodata_index(df):
    geodata_index = {}
    for row in df.itertuples():
        d = dict(row._asdict())

        shapely_polygon_list = shape_to_shapely_polygon_list(d['geometry'])
        multipolygon = shapely_polygon_list_to_multipolygon(
            shapely_polygon_list,
        )

        del d['geometry']
        geodata_index[d['id']] = d | {
            'multipolygon': multipolygon,
        }

    return ds.sort_dict_by_key(geodata_index)
