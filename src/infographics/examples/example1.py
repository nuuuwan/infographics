from infographics.Infographic import Infographic
from infographics.LKMap import LKMap

Infographic(
    title='Sri Lanka',
    children=[LKMap()],
).save('/tmp/infographics.example1.png')
