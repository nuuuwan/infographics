from infographics._utils import log
from infographics.core.SizeSpace import SizeSpace
from infographics.core.SVGPalette import SVGPalette

DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING = 1200, 675, 20
DEFAULT_BASE_FONT_SIZE = 16


class Infographic(SizeSpace, SVGPalette):
    def __init__(
        self,
        title='Title',
        subtitle='Subtitle',
        footer_text='Footer Text',
        child_list=[],
        size=(DEFAULT_WIDTH, DEFAULT_HEIGHT, PADDING),
        base_font_size=DEFAULT_BASE_FONT_SIZE,
    ):
        self.title = title
        self.subtitle = subtitle
        self.footer_text = footer_text
        self.title = title
        self.child_list = child_list
        self.size = size
        self.base_font_size = base_font_size

    def __xml__(self):
        return self.draw_svg([
            self.draw_rect(),
            self.draw_line((-1, 0), (1, 0)),
            self.draw_line((0, -1), (0, 1)),

            self.draw_text(self.title, (0, 0.9), 2),
            self.draw_text(self.subtitle, (0, 0.8), 1),
            self.draw_text(self.footer_text, (0, -0.9), 1),
        ] + [child.__xml__() for child in self.child_list])

    def save(self, svg_file):
        self.__xml__().store(svg_file)
        log.info(f'Saved {svg_file}')
