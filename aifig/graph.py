from aifig import element, draw


class Graph:

    elements = []
    SPACING = 32
    name = None

    def __init__(self, name, elements=None, spacing=32):
        if elements is None:
            elements = []
        self.elements = elements
        self.SPACING = spacing
        self.name = name

    def add(self, layer):
        self.elements.append(layer)

    def _draw(self, debug=False):

        # 256 by default, makes everything less than this appear smaller
        MAX_DENSE_NODES = 256
        MAX_CONV_FILTERS = 1

        for l in self.elements:
            if isinstance(l, element.Dense):
                MAX_DENSE_NODES = max(l.size, MAX_DENSE_NODES)
            if isinstance(l, element.Conv):
                MAX_CONV_FILTERS = max(l.size, MAX_CONV_FILTERS)

        DRAW_X = 0
        DRAW_Y = 0
        prev = None

        for l in self.elements:
            if isinstance(l, element.Padding):
                DRAW_X += l.width
                continue
            # Needs max nodes for relative sizes
            if isinstance(l, element.Dense):
                l.max_size = MAX_DENSE_NODES
            if isinstance(l, element.Conv):
                l.max_size = MAX_CONV_FILTERS

            w = l.draw(DRAW_X, DRAW_Y)

            if debug:
                draw.text(type(l).__name__, DRAW_X, DRAW_Y - 4, italic=True, color="red")
                draw.rect(DRAW_X - 1, DRAW_Y - 1, w + 2, draw.height() + 2, stroke="red", fill="none")

            if prev is not None:
                prev.attach(l)
            DRAW_X += w + self.SPACING
            prev = l

        if debug:
            draw.rect(-2, -2, DRAW_X + 4, draw.height() + 4, stroke="blue", fill="none")

        return DRAW_X