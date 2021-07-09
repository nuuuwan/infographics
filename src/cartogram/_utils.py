"""Utils."""

import logging

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cartogram')


def draw_text(
    xy,
    text,
    verticalalignment='center',
    horizontalalignment='center',
    fontname='Futura',
    fontsize=12,
):
    """Draw text."""
    x, y = xy
    plt.text(
        x,
        y,
        text,
        verticalalignment=verticalalignment,
        horizontalalignment=horizontalalignment,
        fontsize=fontsize,
        fontname=fontname,
    )


def draw_circle(
    cxy,
    r,
    fill='lightgray',
    stroke='gray',
    stroke_width=0.2,
):
    """Draw circle."""
    ax = plt.gca()
    do_fill = fill is not None
    ax.add_patch(
        plt.Circle(
            cxy,
            r,
            edgecolor=stroke,
            facecolor=fill,
            linewidth=stroke_width,
            fill=do_fill,
        )
    )


def draw_color_legend(labels_and_colors):
    """Draw color legend."""
    patches = []
    for label, color in labels_and_colors:
        patches.append(
            Patch(
                color=color,
                label=label,
            )
        )
    plt.legend(handles=patches)


def draw_infographic(
    title,
    subtitle,
    footer_text,
    image_file,
    func_plot_inner,
):
    """Draw infographic."""
    plt.axes([0, 0, 1, 1])
    draw_text((0.5, 0.95), title, fontsize=24)
    draw_text((0.5, 0.9), subtitle, fontsize=12)
    draw_text((0.5, 0.05), footer_text, fontsize=8)

    ax_inner = plt.axes([0.1, 0.1, 0.8, 0.8])
    func_plot_inner(ax_inner)

    fig = plt.gcf()
    fig.set_size_inches(16, 9)
    plt.savefig(image_file)
