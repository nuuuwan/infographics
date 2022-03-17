
from infographics.view.ColoredView import KEY_TO_COLOR
from infographics.view.DorlingView import DorlingView

CIRLCE_RADIUS_MAX_LABEL_VALUE = 0.2


class FlagDorlingView(DorlingView):
    def render_dorling_object(self, id, xy, r, attribs):
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

        x, y = xy
        rx = r
        ry = rx * 9 / 16

        x0 = x - rx
        y0 = y + ry
        inner_list = []
        for [color, p] in [
            [KEY_TO_COLOR['sl_moor'], p_moor],
            [KEY_TO_COLOR['sl_tamil'], p_tamil],
            [KEY_TO_COLOR['buddhist'], p_sinhalese * p_buddhist],
            [KEY_TO_COLOR['sinhalese'], p_sinhalese * (1 - p_buddhist)],
        ]:
            rx0 = rx * p
            inner_list.append(
                self.palette.draw_rect(
                    (x0, y0),
                    (rx0 * 2, ry * 2),
                    {
                        'fill': color,
                        'stroke': 'black',
                        'stroke-width': 0.1,
                        'fill-opacity': 1,
                    },
                )
            )
            x0 += rx0 * 2

        return self.palette.draw_g(inner_list)
