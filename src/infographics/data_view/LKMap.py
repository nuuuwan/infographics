
from infographics.data import LKGeoData
from infographics.data_view.GeoMap import GeoMap


class LKMap(GeoMap):
    def __init__(
        self,
        region_id,
        subregion_type,
        get_color_value,
        legend_title,
        color_palette,
        get_label_data,
        class_view,
    ):
        class_geodata = LKGeoData

        get_color_value = get_color_value \
            if get_color_value else self.get_color_value
        get_label_data = get_label_data \
            if get_label_data else self.get_label_data

        GeoMap.__init__(
            self,
            region_id,
            subregion_type,
            get_color_value,
            legend_title,
            color_palette,
            get_label_data,
            class_geodata,
            class_view,
        )

    def get_color_value(self, id):
        return self.geodata.data[id]['population'] / \
            self.geodata.data[id]['area']

    def get_label(self, id):
        d = self.geodata.data[id]
        return d | {
            'label': d['name'],
            'label_value': d['population'],
        }
