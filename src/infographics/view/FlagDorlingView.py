
from infographics.view.ColoredView import KEY_TO_COLOR
from infographics.view.DorlingView import DorlingView

CIRLCE_RADIUS_MAX_LABEL_VALUE = 0.2


class FlagDorlingView(DorlingView):
    def render_dorling_object(self, id, xy, r, attribs):
        x, y = xy
        rx = r * 0.7
        ry = rx
        label_data = self.get_label_data(id)
        n_sinhalese = label_data['sinhalese']
        n_tamil = (label_data['sl_tamil'] + label_data['ind_tamil'])
        n_moor = (label_data['sl_moor'] + label_data['malay'])
        n_buddhist = (label_data['buddhist'])

        total = n_sinhalese + n_tamil + n_moor
        p_sinhalese = n_sinhalese / total
        p_tamil = n_tamil / total
        p_moor = n_moor / total
        p_buddhist = n_buddhist / n_sinhalese

        rx0 = rx * p_moor
        rx1 = rx * p_tamil
        rx2 = rx * p_sinhalese

        x0 = 0
        x1 = rx0 * 2
        x2 = (rx0 + rx1) * 2

        return self.palette.draw_g([
            self.palette.draw_rect(
                (x - rx + x0, y + ry),
                (rx0 * 2, ry * 2),
                {'fill': KEY_TO_COLOR['sl_moor'], 'opacity': 1},
            ),
            self.palette.draw_rect(
                (x - rx + x1, y + ry),
                (rx1 * 2, ry * 2),
                {'fill': KEY_TO_COLOR['sl_tamil'], 'opacity': 1},
            ),
            self.palette.draw_rect(
                (x - rx + x2, y + ry),
                (rx2 * 2, ry * 2),
                {'fill': KEY_TO_COLOR['sinhalese'], 'opacity': 1},
            ),
            self.palette.draw_rect(
                (
                    x - rx + x2 + rx2 * (1 - p_buddhist),
                    y + ry - ry * (1 - p_buddhist)
                ),
                (rx2 * 2 * p_buddhist, ry * 2 * p_buddhist),
                {'fill': KEY_TO_COLOR['buddhist'], 'opacity': 1},
            ),
        ])
