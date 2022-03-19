DEFAULT_FONT = 'Gill Sans'


DEFAULT_BORDERED_AREA = {
    'fill': 'white',
    'stroke': 'lightgray',
    'stroke-width': 1,
}


class SVG_STYLES:
    SVG = {
        'xmlns': 'http://www.w3.org/2000/svg',

    }

    TEXT = {
        'fill': 'black',
        'stroke': 'none',
        'text-anchor': 'middle',
        'dominant-baseline': 'middle',
        'font-family': DEFAULT_FONT,
    }

    RECT = DEFAULT_BORDERED_AREA

    CIRCLE = DEFAULT_BORDERED_AREA

    LINE = {
        'stroke': 'lightgray',
        'stroke-width': 1,
        'opacity': 0.2,
    }

    PATH = DEFAULT_BORDERED_AREA
