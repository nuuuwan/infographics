"""Utils."""

import logging

from matplotlib.patches import Patch

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('cartogram')


def draw_color_legend(plt, labels_and_colors):
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
