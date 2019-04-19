from aifig import draw


class Element:

    def draw(self, x, y):
        return 0

    def attach(self, neighbor):
        pass


class Padding(Element):

    width = 0

    def __init__(self, width):
        self.width = width


class Arrow(Element):

    label = None
    comment = None

    def __init__(self, label=None, comment=None):
        self.label = label
        self.comment = comment

    def draw(self, x, y):
        w, h = draw.arrow(x, y + draw.mid())
        self.left = (x, y + draw.mid())
        self.right = (x + w, y + draw.mid())
        if self.label is not None:
            draw.text(self.label, x + w / 2, y + draw.mid() + h / 2 + 12, center=True)
        if self.comment is not None:
            draw.text(self.comment, x + w / 2, y + draw.mid() + h / 2 + 22, center=True, italic=True, color="gray")
        return w

    def attach(self, neighbor):
        pass


class Dense(Element):

    label = None
    size = 1
    size_label = False

    max_size = 1

    attach_top = (0,0)
    attach_bot = (0,0)

    circle_positions = []

    simple = False

    pad = 8

    def __init__(self, label=None, size=1, comment=None, size_label=True, simple=False):
        self.label = label
        self.simple = simple
        self.comment = comment
        self.size = size
        self.size_label = size_label
    
    def draw(self, x, y):

        x += self.pad

        # Relative scale
        scale = self.size / self.max_size*0.75 + 0.25
        sy = y + draw.height() * (1 - scale) / 2
        sx = x

        if self.simple:
            w, h = draw.rect(x + 4, sy, 8, draw.height() * scale)
        else:
            w, h = 16, draw.height() * scale
            n_nodes = int(draw.height() * scale / 8)

            if self.size <= 3:
                n_nodes = self.size

            offy = (h - n_nodes*10)/2
            self.circle_positions = []
            for i in range(n_nodes):
                draw.circle(x + 8, sy + i * 10 + 4 + offy, 4)
                self.circle_positions.append((x+8, sy+i*10+4+offy))

            sy += offy
            h -= offy-1
            sx += 6
            x -= 2

        if self.label is not None:
            draw.text(self.label, x + w / 2 + 2, sy + h + 10, center=True)
        if self.comment is not None:
            draw.text(self.comment, x + w / 2 + 2, sy + h + 20, center=True, italic=True, color="gray")
        if self.size_label:
            draw.text(str(self.size), x + w / 2 + 2, sy - 5, center=True, italic=True, color="gray")

        # Attachment positions
        self.top_left = (sx, sy)
        self.bot_left = (sx, sy+h)
        self.top_right = (sx+12, sy)
        self.bot_right = (sx+12, sy+h)

        return w + self.pad*2

    def attach(self, neighbor):
        if isinstance(neighbor, Dense):
            if not self.simple and not neighbor.simple:
                # Connect every node with dots
                for cp in self.circle_positions:
                    for cp2 in neighbor.circle_positions:
                         draw.line(*cp, *cp2, stroke="gray")
                # Fill in white circles (lines should be behind)
                for cp in self.circle_positions:
                    draw.circle(*cp, 4, fill="white")
                for cp in neighbor.circle_positions:
                    draw.circle(*cp, 4, fill="white")
            else:
                draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
                draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")
        if isinstance(neighbor, Image):
            if not self.simple:
                # Connect every node with dots
                for cp in self.circle_positions:
                     draw.line(*cp, *neighbor.top_left, stroke="gray")
                     draw.line(*cp, *neighbor.top_right, stroke="gray")
                # Fill in white circles (lines should be behind)
                for cp in self.circle_positions:
                    draw.circle(*cp, 4, fill="white")
            else:
                draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
                draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")
        if isinstance(neighbor, Arrow):
            if not self.simple:
                # Connect every node with dots
                for cp in self.circle_positions:
                    draw.line(*cp, *neighbor.left, stroke="gray")
                # Fill in white circles (lines should be behind)
                for cp in self.circle_positions:
                    draw.circle(*cp, 4, fill="white")
            else:
                draw.line(*self.top_right, *neighbor.left, stroke="gray")
                draw.line(*self.bot_right, *neighbor.left, stroke="gray")
        if isinstance(neighbor, Conv):
            draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
            draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")


class Conv(Element):

    max_size = 1

    def __init__(self, label=None, size=32, size_label=True, comment=None):
        self.label = label
        self.comment = comment
        self.size = size
        self.size_label = size_label

    def draw(self, x, y):
        
        # Relative scale
        scale = self.size / self.max_size * 0.25 + 0.75
        # Max 16 nodes in figure
        nodes = int(min(max(20*scale, 1), 20))

        if self.size <= 20:
            nodes = self.size

        width = nodes * 4 + 20
        height = nodes * 4 + 20

        sy = y + (draw.height() - height) / 2

        for i in range(nodes):
            f = "#eeeeee" if not (i+nodes%2) % 2 else "white"
            draw.rect(x + i * 4, sy + i * 4, 24, 24, fill=f)

        # Attachment positions
        self.top_left = (x, sy)
        self.top_right = (x+24, sy)
        self.bot_left = (x+width-24, sy+height)
        self.bot_right = (x+width, sy+height)
        self.center = (x+width/2-18, sy+height/2+4)

        # Label
        if self.label is not None:
            draw.text(self.label, x + width - 12, sy + height + 10, center=True)
        # Comment
        if self.comment is not None:
            draw.text(self.comment, x + width - 12, sy + height + 20, center=True, italic=True, color="gray")

        # Size label
        if self.size_label:
            # draw.line(x+24+8, sy, x+width, sy+height-24-8, stroke="gray")
            draw.text(str(self.size), x + width / 2 + 16, sy + height / 2 - 16, italic=True, color="gray")

        return width

    def attach(self, neighbor):
        if isinstance(neighbor, Dense) or isinstance(neighbor, Image):
            draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
            draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")
        if isinstance(neighbor, Conv) or isinstance(neighbor, Pool):
            x, y = self.bot_left
            draw.rect(x + 4, y - 12, 8, 8, stroke="gray")
            draw.line(x + 4, y - 12, *neighbor.center, stroke="gray")
            draw.line(x + 12, y - 4, *neighbor.center, stroke="gray")


class Image(Element):

    def __init__(self, label=None, comment=None):
        self.label = label
        self.comment = comment

    def draw(self, x, y):
        
        width = 48
        height = 48

        sy = y + (draw.height() - height) / 2

        draw.rect(x, sy, width, height, fill="#eeeeee")
        
        # Label
        if self.label is not None:
            draw.text(self.label, x + width / 2, sy + height + 10, center=True)
        if self.comment is not None:
            draw.text(self.comment, x + width / 2, sy + height + 20, center=True, italic=True, color="gray")

        # Attachment positions
        self.top_right = (x+width, sy)
        self.top_left = (x, sy)
        self.bot_left = (x, sy+height)
        self.bot_right = (x+width, sy+height)

        return width

    def attach(self, neighbor):
        if isinstance(neighbor, Dense):
            draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
            draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")
        if isinstance(neighbor, Conv):
            x, y = self.bot_left
            draw.rect(x + 4, y - 12, 8, 8, stroke="gray")
            draw.line(x + 4, y - 12, *neighbor.center, stroke="gray")
            draw.line(x + 12, y - 4, *neighbor.center, stroke="gray")


class Pool(Element):

    def __init__(self, label=None, comment=None):
        self.label = label
        self.comment = comment

    def draw(self, x, y):
        
        big_rect = 32
        small_rect = 24

        sy = y + draw.mid() - 20

        xp = x+10
        yp = sy

        # Big pool square
        for i in range(4):
            for j in range(4):
                f = "white" if (i+j)%2 else "white"
                draw.rect(xp, yp, big_rect / 4, big_rect / 4, stroke="gray")
                xp += big_rect/4
            yp += big_rect/4
            xp = 10+x

        xp = 10+x+big_rect/2.5
        yp = sy+big_rect/2.5

        # Small pool square
        for i in range(2):
            for j in range(2):
                f = "white" if (i+j)%2 else "#eeeeee"
                draw.rect(xp, yp, small_rect / 2, small_rect / 2, fill=f)
                xp += small_rect/2
            yp += small_rect/2
            xp = 10+x+big_rect/2.5

        # Label
        if self.label is not None:
            draw.text(self.label, 10 + x + big_rect / 2 + 2, sy + 48, center=True)
        # Comment
        if self.comment is not None:
            draw.text(self.comment, 10 + x + big_rect / 2 + 2, sy + 58, center=True, italic=True, color="gray")

        # Attachment
        self.top_right = (x+big_rect+10, sy)
        self.bot_right = (x+big_rect+14, sy+big_rect+5)
        self.center = (x+big_rect/2, sy+big_rect/2)

        return big_rect+small_rect*0.25+20

    def attach(self, neighbor):
        if neighbor.top_left is not None and neighbor.bot_left is not None:
            draw.line(*self.top_right, *neighbor.top_left, stroke="gray")
            draw.line(*self.bot_right, *neighbor.bot_left, stroke="gray")
