from infographics.core import Infographic
from infographics.data_view import LKCensusMap

Infographic(
    title='Sinhalese Population',
    subtitle='Provinces of Sri Lanka',
    footer_text='visualization by @nuuuwan',
    child_list=[LKCensusMap(
        subregion_type='district',
    )]
).save('/tmp/infographics.example3.svg')
