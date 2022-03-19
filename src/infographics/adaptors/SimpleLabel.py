from infographics.core.SVGPalette import SVGPalette


class SimpleLabel:
    def __init__(self, get_id_to_label_label):
        self.get_id_to_label_label = get_id_to_label_label

    def get_id_to_label(self, id, cxy, rxy):
        palette = SVGPalette()
        label = self.get_id_to_label_label(id)
        rx, ry = rxy
        font_size = palette.actual_width * rx / len(label) / 16
        return palette.draw_text(
            label,
            cxy,
            font_size,
        )
