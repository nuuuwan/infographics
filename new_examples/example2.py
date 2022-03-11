from infographics.core import Infographic
from infographics.geo import LKMap

Infographic(
    child_list=[
        LKMap(),
    ]
).save('/tmp/infographics.example2.svg')
