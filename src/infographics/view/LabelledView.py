from infographics.core import SVGPalette


class LabelledView:
    def __init__(
        self,
        keys,
        get_label_data,
        get_label_xy,
        get_label_r,
    ):

        self.keys = keys
        self.get_label_data = get_label_data
        self.get_label_xy = get_label_xy
        self.get_label_r = get_label_r

        self.palette = SVGPalette()

    def __xml__(self):
        inner_list = []
        for id in self.keys():
            inner_list.append(
                self.palette.draw_g(
                    self.render_label(id),
                ),
            )
        return self.palette.draw_g(inner_list)

    def render_label(self, id):
        label_data = self.get_label_data(id)
        label = label_data['label']
        r = self.get_label_r(id)
        (x, y) = self.get_label_xy(id)

        relative_font_width = r * 2 * \
            self.palette.actual_width / SVGPalette.DEFAULT_BASE_FONT_SIZE
        relative_font_size = min(0.8, relative_font_width / len(label))

        # if relative_font_size < 1:
        #     return []

        return [
            # self.palette.draw_text(
            #     format.as_number(label_value),
            #     (x, y + 0.075 * relative_font_size),
            #     relative_font_size,
            #     {'font-weight': 'bold'},
            # ),
            self.palette.draw_text(
                label,
                (x, y + r),
                relative_font_size * 0.8,
            ),
        ]
