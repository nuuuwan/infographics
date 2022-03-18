from infographics.core import SVGPalette

CIRCLE_R_LEGEND = 0.02


class LegendView:

    def __init__(
        self,
        legend_title,
        color_values,
        get_color_value_to_color,

    ):
        self.legend_title = legend_title
        self.color_values = color_values
        self.get_color_value_to_color = get_color_value_to_color
        self.palette = SVGPalette()

    def render_row(self, color_value, xy):
        color = self.get_color_value_to_color(color_value)

        x, y = xy
        return self.palette.draw_g([
            self.palette.draw_circle(
                (x + CIRCLE_R_LEGEND, y + CIRCLE_R_LEGEND / 2),
                CIRCLE_R_LEGEND,
                {'fill': color},
            ),
            self.palette.draw_text(
                color_value,
                (x + CIRCLE_R_LEGEND * 3, y),
                1,
                {'text-anchor': 'start'},
            ),
        ])

    def __xml__(self):
        x0, y0 = 0.5, 0.5
        inner_list = [
            self.palette.draw_text(
                self.legend_title, (x0, y0), 1, {
                    'text-anchor': 'start'},)]
        for i, color_value in enumerate(self.color_values):
            y = y0 - ((i + 1.5) * 0.05)
            inner_list.append(self.render_row(color_value, (x0, y)))
        return self.palette.draw_g(inner_list)
