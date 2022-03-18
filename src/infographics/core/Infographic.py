from infographics._utils import log
from infographics.core.SVGPalette import SVGPalette


class Infographic:
    def __init__(
        self,
        title='Title',
        subtitle='Subtitle',
        footer_text='Created with https://github.com/nuuuwan/infographics',
        children=[],
    ):
        self.title = title
        self.subtitle = subtitle
        self.footer_text = footer_text
        self.title = title
        self.children = children

    def __xml__(self):
        palette = SVGPalette()
        return palette.draw_svg([
            palette.draw_rect(),
        ] + [child.__xml__() for child in self.children] + [
            palette.draw_text(self.title, (0, 0.9), 2),
            palette.draw_text(self.subtitle, (0, 0.8), 1),
            palette.draw_text(self.footer_text, (0, -0.9), 0.67),
        ])

    def save(self, svg_file):
        self.__xml__().store(svg_file)
        log.info(f'Saved {svg_file}')
