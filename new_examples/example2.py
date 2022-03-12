from infographics.core import Infographic
from infographics.view import LKMap

Infographic(
    title='Provinces',
    subtitle='of Sri Lanka',
    footer_text='visualization by @nuuuwan',
    child_list=[
        LKMap(),
    ]
).save('/tmp/infographics.example2.svg')
