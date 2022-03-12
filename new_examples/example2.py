from infographics.core import Infographic
from infographics.data_view import LKMap

Infographic(
    title='Population & Population Density',
    subtitle='Provinces of Sri Lanka',
    footer_text='visualization by @nuuuwan',
    child_list=[
        LKMap(
            region_id='LK',
            subregion_type='district',
            legend_title='Population Density (people per km²)',
        ),
    ]
).save('/tmp/infographics.example2.svg')
