from infographics.data import LKCensusData
from infographics.data_view.LKMap import LKMap


class LKCensusMap:
    def __init__(
        self,
        # LKCensusData
        table_id,

        # LKMap
        region_id,
        subregion_type,
        legend_title,
        color_palette,
        class_view,

        # LKCensusMap
        field,

    ):
        self.field = field
        self.data = LKCensusData(table_id)
        self.view = LKMap(
            region_id,
            subregion_type,
            self.get_color_value,
            legend_title,
            color_palette,
            self.get_label,
            self.get_label_value,
            class_view,
        )

    def __xml__(self):
        return self.view.__xml__()

    # Implement AbstractColoredView
    def get_color_value(self, id):
        d = self.data.data[id]
        return d[self.field] / d[self.data.total_field]

    # For AbstractLabelledView
    def get_label(self, id):
        return self.view.geodata.data[id]['name']

    def get_label_value(self, id):
        return self.get_color_value(id)
