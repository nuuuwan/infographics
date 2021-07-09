from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

Infographic(
    title='Sri Lanka',
    children=[LKMap(region_id='LK', sub_region_type='district')],
).save('/tmp/infographics.example2.png')
