from abc import ABC, abstractmethod

from utils.xmlx import _

from infographics.core.SVG_STYLES import SVG_STYLES


class SVGPalette(ABC):
    @abstractmethod
    def __xml__(self):
        pass

    def get_font_size(self, relative_font_size):
        return self.base_font_size * relative_font_size

    def draw_text(self, inner, p=(0, 0), relative_font_size=1):
        x, y = self.t(p)
        return _('text', inner, SVG_STYLES.TEXT | {
            'x': x,
            'y': y,
            'font-size': self.get_font_size(relative_font_size),
        })

    def draw_line(self, p1=(-1, 0), p2=(1, 0)):
        x1, y1 = self.t(p1)
        x2, y2 = self.t(p2)
        return _('line', None, SVG_STYLES.LINE | {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        })

    def draw_rect(self, p0=(-1, 1), size=(2, 2)):
        x0, y0 = self.t(p0)
        x1, y1 = self.t((p0[0] + size[0], p0[1] - size[1]))
        width = x1 - x0
        height = y1 - y0
        return _('rect', None, SVG_STYLES.RECT | {
            'x': x0,
            'y': y0,
            'width': width,
            'height': height,

        })

    def draw_svg(self, child_list):
        return _(
            'svg',
            child_list,
            SVG_STYLES.SVG | {
                'width': self.width,
                'height': self.height})