from infographics.core import Infographic
from infographics.data import LKElectionsData
from infographics.view import BarGraphBasic

if __name__ == '__main__':
    data = [
        [1994, [[1, 'JVP (SLPF)']]],
        [2000, [[10, 'JVP']]],
        [2001, [[16, 'JVP']]],
        [2004, [[39, 'JVP (UPFA)']]],
        [2010, [[4, 'JVP (DNA)'], [3, 'NFF (UPFA)']]],
        [2015, [[6, 'JVP'], [5, 'NFF (UPFA)']]],
        [2020, [[3, 'JVP (NPP)'], [6, 'NFF (SLPFA)']]],
    ]
    Infographic(
        'JVP and related parties',
        'Seats in the Sri Lankan Parliament (Since 1999)',
        LKElectionsData.SOURCE_TEXT,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[
            BarGraphBasic(data),
        ],
    ).save('/tmp/infographics.example11.svg')
