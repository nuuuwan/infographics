
from utils import colorx
from utils.xmlx import _

from infographics.core.SVG_STYLES import SVG_STYLES
from infographics.core.SVGPalettePolygon import SVGPalettePolygon
from infographics.core.SVGPaletteSize import SVGPaletteSize

DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING = 1200, 675, 20
DEFAULT_BASE_FONT_SIZE = 16


class SVGPalette(SVGPaletteSize, SVGPalettePolygon):
    def __init__(
        self,
        size=(DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING),
        base_font_size=DEFAULT_BASE_FONT_SIZE,
    ):
        self.size = size
        self.base_font_size = base_font_size

    def get_font_size(self, relative_font_size):
        return self.base_font_size * relative_font_size

    def draw_text(self, inner, p=(0, 0), relative_font_size=1, attribs={}):
        x, y = self.t(p)
        return _('text', inner, SVG_STYLES.TEXT | {
            'x': x,
            'y': y,
            'font-size': self.get_font_size(relative_font_size),
        } | attribs)

    def draw_line(self, p1=(-1, 0), p2=(1, 0), attribs={}):
        x1, y1 = self.t(p1)
        x2, y2 = self.t(p2)
        return _('line', None, SVG_STYLES.LINE | {
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
        } | attribs)

    def draw_circle(self, pc, pr=0.1, attribs={}):
        cx, cy = self.t(pc)
        cx1, ___ = self.t((pc[0] + pr, pc[1]))
        r = abs(cx1 - cx)
        return _('circle', None, SVG_STYLES.CIRCLE | {
            'cx': cx,
            'cy': cy,
            'r': r,
        } | attribs)

    def draw_rect(self, p0=(-1, 1), size=(2, 2), attribs={}):
        x0, y0 = self.t(p0)
        x1, y1 = self.t((p0[0] + size[0], p0[1] - size[1]))
        width = x1 - x0
        height = y1 - y0
        return _('rect', None, SVG_STYLES.RECT | {
            'x': x0,
            'y': y0,
            'width': width,
            'height': height,
        } | attribs)

    def draw_svg(self, child_list, attribs={}):
        return _(
            'svg',
            child_list,
            SVG_STYLES.SVG | {
                'width': self.width,
                'height': self.height} | attribs)

    def draw_g(self, child_list, attribs={}):
        return _('g', child_list, attribs)

    @staticmethod
    def get_random_color_list(n):
        return [colorx.random_hex() for i in range(0, n)]
