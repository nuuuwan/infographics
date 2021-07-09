"""Infographic."""

import os

import matplotlib.pyplot as plt
import plotx
from _utils import log


class Infographic:
    def __init__(
        self,
        children=[],
        title='',
        subtitle='',
        footer_text='infographics-nuuuwan',
        size=(16, 9),
    ):
        plt.axes([0, 0, 1, 1])
        plotx.draw_text((0.5, 0.95), title, fontsize=24)
        plotx.draw_text((0.5, 0.9), subtitle, fontsize=12)
        plotx.draw_text(
            (0.5, 0.05),
            footer_text,
            fontsize=8,
            fontcolor='gray',
        )

        fig = plt.gcf()
        fig.set_size_inches(*size)

        for child in children:
            child.draw()

    def save(self, image_file):
        plt.savefig(image_file)
        log.info('Saved infographic to %s', image_file)
        os.system('open %s' % image_file)
        return self

    def close(self):
        plt.close()
        return self


if __name__ == '__main__':
    Infographic().save('/tmp/infographics.infographic.png').close()
