
import svgwrite
from aifig import draw


class Figure:

    _figure = None
    _connections = []
    _graphs = [[None for _ in range(10)] for _ in range(10)]
    _step_draw_position = 0

    title = None
    author = None

    _PADDING = 32
    _V_SPACING = 48
    _H_SPACING = 16

    _width = 100
    _height = 100

    def __init__(self, title=None, author=None):
        self.filename = "figure.svg"
        self.title = title
        self.author = author
        self._figure = svgwrite.Drawing(self.filename)

    def add(self, graph, x=0, y=None):
        if x > 9 or x < 0 or (y is not None and (y > 9 or y < 0)):
            print("Warning: cannot add graph to figure at position {}, {} - coordinates must be between 0-9!".format(x,
                                                                                                                     y or "?"))
            return
        if y is None:
            found_spot = False
            for i in range(len(self._graphs[x])):
                if self._graphs[x][i] is None:
                    self._graphs[x].append(graph)
                    found_spot = True
                    break
            if not found_spot:
                print("Warning: could not add graph at x=", x, ", no more space in column!")
        else:
            if self._graphs[x][y] is not None:
                print("Warning: graph at {}, {} was overwritten".format(x, y))
            self._graphs[x][y] = graph

    def connect(self, name, name2, position=None, offset=0):
        x, y, x2, y2 = -1, 0, -1, 0
        for i in range(10):
            for j in range(10):
                if self._graphs[i][j] is not None:
                    if name == self._graphs[i][j].name:
                        x = i
                        y = j
                    if name2 == self._graphs[i][j].name:
                        x2 = i
                        y2 = j
        if x is -1:
            print("Warning: could not find graph {} to connect".format(name))
            return
        elif x2 is -1:
            print("Warning: could not find graph {} to connect".format(name2))
            return

        self._connections.append((x, y, x2, y2, position, offset))

    def _draw(self, debug=False):

        self._width = 0
        self._height = 0
        GRAPH_POSITIONS = [[(0, 0, 0, 0) for _ in range(10)] for _ in range(10)]

        for y in range(10):
            self._step_draw_position = 0
            for x in range(10):
                graph = self._graphs[x][y]
                # Draw at correct position
                if graph is None:
                    continue

                draw.begin(self._figure)
                gw = graph._draw(debug)

                # Calculate translation
                x_translate = self._PADDING + self._H_SPACING * x
                x_translate += self._step_draw_position
                y_translate = (draw.height() + self._V_SPACING) * y + self._PADDING / 2

                if self.title is not None:
                    y_translate += 30
                if self.author is not None:
                    y_translate += 10

                # Add to group and translate in figure
                group = self._figure.g()
                draw.add_all(group)
                group.translate(x_translate, y_translate)
                self._figure.add(group)

                GRAPH_POSITIONS[x][y] = (x_translate, y_translate, gw)

                self._step_draw_position += gw

                self._width = max(self._width, self._step_draw_position + self._PADDING)
                self._height = max(self._height, y_translate + draw.height() + self._PADDING)

        self._width += self._PADDING / 4

        # Draw connections
        draw.begin(self._figure)
        for con in self._connections:

            x, y, x2, y2, position, offset = con

            from_x, from_y, from_w = GRAPH_POSITIONS[x][y]
            to_x, to_y, to_w = GRAPH_POSITIONS[x2][y2]

            from_x += from_w - 16
            from_y += draw.height() / 2
            to_y += draw.height() / 2

            # First out
            draw.line(from_x - 16, from_y, from_x + 12, from_y, stroke="gray")
            # Arrowhead
            draw.line(to_x - 6, to_y - 5, to_x - 1, to_y, stroke="gray")
            draw.line(to_x - 6, to_y + 5, to_x - 1, to_y, stroke="gray")

            if y < y2:
                mid = to_y - draw.height() / 2 - self._V_SPACING / 2
            else:
                mid = to_y + draw.height() / 2 + self._V_SPACING / 2

            if position is not None:
                mid = (draw.height() + self._V_SPACING) * position + self._PADDING / 2 - self._V_SPACING / 2
                if self.title is not None:
                    mid += 30
                if self.author is not None:
                    mid += 10
            if offset is not None:
                mid += offset

            draw.line(from_x + 12, from_y, from_x + 12, mid, stroke="gray")
            draw.line(from_x + 12, mid, to_x - 16, mid, stroke="gray")
            draw.line(to_x - 16, mid, to_x - 16, to_y, stroke="gray")
            draw.line(to_x - 16, to_y, to_x - 1, to_y, stroke="gray")

        draw.add_all(self._figure)

    def _save(self, debug=False):
        self._step_draw_position = 0
        self._draw(debug)
        if self.title is not None:
            draw.begin(self._figure)
            draw.title(self.title, self._PADDING, self._PADDING)
            draw.add_all(self._figure, 0)
        if self.author is not None:
            draw.begin(self._figure)
            draw.text(self.author, self._PADDING, self._PADDING + 10, color="gray", italic=True)
            draw.add_all(self._figure, 0)
        self._figure.width = self._width
        self._figure.height = self._height
        self._figure.viewbox(0, 0, self._width, self._height)
        self._figure.save()

    def save_svg(self, path="figure.svg", debug=False):
        self._figure.filename = path
        self._save(debug=debug)
        print("Saved figure as", self.filename)
        self._figure.filename = "figure.svg"

    def save_png(self, path="figure.png", scale=1):
        self.filename = path
        self._save_custom(scale * 3, "png")
        print("Saved figure as", self.filename)
        self.filename = "figure.svg"

    def save_pdf(self, path="figure.pdf"):
        self.filename = path
        self._save_custom(1, "pdf")
        print("Saved figure as", self.filename)
        self.filename = "figure.svg"

    def _save_custom(self, scale=5, format="pdf"):

        self._figure.filename = "._tmp_model_fig.svg"
        self._figure.stroke(width=scale * 1.25)
        self._save()
        self._figure.stroke(width=1)
        self._figure.filename = self.filename

        import os

        try:
            from svglib.svglib import svg2rlg
        except:
            print("Error: svglib not found (required for {} export)".format(format))
            print("try 'pip install svglib'")
            os.remove("._tmp_model_fig.svg")
            return

        drawing = svg2rlg("._tmp_model_fig.svg")
        drawing.scale(scale, scale)
        drawing.width = self._width * scale
        drawing.height = self._height * scale

        if format is "pdf":
            from reportlab.graphics import renderPDF
            renderPDF.drawToFile(drawing, self.filename)
        if format is "png":
            from reportlab.graphics import renderPM
            renderPM.drawToFile(drawing, self.filename, fmt="PNG")

        os.remove("._tmp_model_fig.svg")
