from infographics.core import ColorPaletteVaryLightness, Infographic
from infographics.data_view import LKCensusMap

Infographic(
    title='Buddhist Population',
    subtitle='Provinces of Sri Lanka',
    footer_text='visualization by @nuuuwan',
    child_list=[
        LKCensusMap(
            region_id='LK-11',
            subregion_type='dsd',
            table_id='religious_affiliation_of_population',
            field='buddhist',
            color_palette=ColorPaletteVaryLightness(
                hue=60,
                min_lightness=1,
                max_lightness=0.4),
        )]).save('/tmp/infographics.example3.svg')
