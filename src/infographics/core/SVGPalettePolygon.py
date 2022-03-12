
from utils.xmlx import _

from infographics.core.SVG_STYLES import SVG_STYLES

DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING = 1200, 675, 20
DEFAULT_BASE_FONT_SIZE = 16


class SVGPalettePolygon:
    def draw_multi2polygon(self, multi2polygon, attribs={}):
        return self.draw_g(list(map(
            lambda multipolygon: self.draw_multipolygon(
                multipolygon,
                attribs,
            ),
            multi2polygon,
        )), attribs)

    def draw_multipolygon(self, multipolygon, attribs={}):
        return self.draw_g(list(map(
            lambda polygon: self.draw_polygon(polygon, attribs),
            multipolygon,
        )), attribs)

    def draw_polygon(self, polygon, attribs={}):
        d_list = []
        for p in polygon:
            x, y = self.t(p)
            prefix = 'M' if (not d_list) else 'L'
            d_list.append('%s%d,%d' % (prefix, x, y))
        d_list.append('z')
        d = ' '.join(d_list)
        return _('path', None, SVG_STYLES.PATH | {'d': d} | attribs)
