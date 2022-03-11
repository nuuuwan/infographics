from infographics._utils import log
from infographics.core.SVGPalette import SVGPalette


class Infographic:
    def __init__(
        self,
        title='Title',
        subtitle='Subtitle',
        footer_text='Footer Text',
        child_list=[],
    ):
        self.title = title
        self.subtitle = subtitle
        self.footer_text = footer_text
        self.title = title
        self.child_list = child_list

    @property
    def xml(self):
        palette = SVGPalette()
        return palette.draw_svg([
            palette.draw_rect(),
            palette.draw_line((-1, 0), (1, 0)),
            palette.draw_line((0, -1), (0, 1)),

            palette.draw_text(self.title, (0, 0.9), 2),
            palette.draw_text(self.subtitle, (0, 0.8), 1),
            palette.draw_text(self.footer_text, (0, -0.9), 1),
        ] + [child.xml for child in self.child_list])

    def save(self, svg_file):
        self.xml.store(svg_file)
        log.info(f'Saved {svg_file}')
