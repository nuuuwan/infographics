from infographics.core import Infographic
from infographics.data import LKElectionsData

if __name__ == '__main__':
    data = [
        [1994, [[1, 'with SLPF']]],
        [2000, [[10, 'JVP']]],
        [2001, [[16, 'JVP']]],
        [2004, [[39, 'JVP with PA']]],
        [2010, [[4, 'JVP with DNA'], [3, 'NFF with PA']]],
        [2015, [[6, 'JVP'], [5, 'NFF with PA']]],
        [2020, [[3, 'JVP with NPP'], [6, 'NFF with PA']]],
    ]
    Infographic(
        'JVP and related parties',
        'Seats in the Sri Lankan Parliament',
        LKElectionsData.SOURCE_TEXT,
        Infographic.DEFAULT_FOOTER_TEXT,
        children=[]
    ).save('/tmp/infographics.example11.svg')
