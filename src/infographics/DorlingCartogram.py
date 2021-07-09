import math

from infographics import LKMap, dorling_compress, plotx


def _default_func_get_radius_value(row):
    return row.population


def _default_func_format_radius_value(radius_value):
    return '{:,.0f}\npeople'.format(radius_value)


def _func_value_to_color_blank(_):
    return plotx.DEFAULTS.COLOR_FILL


def _func_render_label_blank(*_):
    pass


class DorlingCartogram:
    def __init__(
        self,
        region_id='LK',
        sub_region_type='province',
        func_get_color_value=LKMap._default_func_get_color_value,
        func_value_to_color=LKMap._default_func_value_to_color,
        func_format_color_value=LKMap._default_func_format_color_value,
        func_render_label=LKMap._default_func_render_label,
        func_get_radius_value=_default_func_get_radius_value,
        func_format_radius_value=_default_func_format_radius_value,
        compactness=0.3,
    ):
        self.region_id = region_id
        self.sub_region_type = sub_region_type

        self.func_get_color_value = func_get_color_value
        self.func_value_to_color = func_value_to_color
        self.func_format_color_value = func_format_color_value
        self.func_render_label = func_render_label

        self.func_get_radius_value = func_get_radius_value
        self.func_format_radius_value = func_format_radius_value

        self.compactness = compactness

    def draw(self):
        def _func_render_overlay_dorling(
            gpd_df,
            n_regions,
            minx,
            miny,
            maxx,
            maxy,
            spanx,
            spany,
            area,
        ):
            n_regions = 0
            radius_values = []
            for _, row in gpd_df.iterrows():
                n_regions += 1
                radius_values.append(self.func_get_radius_value(row))
            sum_radius_value = sum(radius_values)
            max_radius_value = max(radius_values)

            alpha = self.compactness * math.pi / 4
            beta = alpha * area / math.pi / sum_radius_value

            points = []
            for i_row, row in gpd_df.iterrows():
                points.append(
                    {
                        'x': row.geometry.centroid.x,
                        'y': row.geometry.centroid.y,
                        'r': math.sqrt(self.func_get_radius_value(row) * beta),
                        'row': row,
                    }
                )

            compressed_points = dorling_compress._compress(
                points,
                (minx, miny, maxx, maxy),
            )

            for point in compressed_points:
                x, y, r, row = point['x'], point['y'], point['r'], point['row']
                color_value = self.func_get_color_value(row)
                color = self.func_value_to_color(color_value)
                plotx.draw_circle((x, y), r, fill=color)
                if n_regions <= 30:
                    self.func_render_label(row, x, y, spany)

            # radius legend
            x, y = (minx + spanx * 0.9), (miny + spany * 0.75)
            radius_value = math.pow(10, round(math.log10(max_radius_value)))
            radius = math.sqrt(radius_value * beta)
            formatted_radius_value = self.func_format_radius_value(radius_value)
            plotx.draw_text((x, y), 'SCALE\n%s' % formatted_radius_value)
            plotx.draw_circle((x, y), radius)

        LKMap.LKMap(
            region_id=self.region_id,
            sub_region_type=self.sub_region_type,
            func_value_to_color=_func_value_to_color_blank,
            func_render_label=_func_render_label_blank,
            func_render_overlay=_func_render_overlay_dorling,
        ).draw()


if __name__ == '__main__':
    from Infographic import Infographic

    Infographic(
        title='Sri Lanka',
        children=[
            DorlingCartogram(region_id='LK', sub_region_type='district'),
        ],
    ).save('/tmp/infographics.lkmap.png').close()
