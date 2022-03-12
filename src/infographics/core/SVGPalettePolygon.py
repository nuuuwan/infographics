
from utils.xmlx import _

from infographics.core.SVG_STYLES import SVG_STYLES

DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING = 1200, 675, 20
DEFAULT_BASE_FONT_SIZE = 16


class SVGPalettePolygon:
    def draw_p_list_list_list(self, p_list_list_list):
        return _('g', list(map(
            self.draw_p_list_list,
            p_list_list_list,
        )))

    def draw_p_list_list(self, p_list_list):
        return _('g', list(map(
            self.draw_p_list,
            p_list_list,
        )))

    def draw_p_list(self, p_list):
        d_list = []
        for p in p_list:
            x, y = self.t(p)
            prefix = 'M' if (not d_list) else 'L'
            d_list.append('%s%d,%d' % (prefix, x, y))
        d_list.append('z')
        d = ' '.join(d_list)
        return _('path', None, SVG_STYLES.PATH | {'d': d})
