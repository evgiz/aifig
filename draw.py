
_figure_ref = None

shape_group = None
text_group = None
text_group_title = None
text_group_italic = None

FIGURE_ARROW = [
    (0, -.3), (1, -.3), (1, -.75), (1.75, 0),
    (1, .75), (1, .3), (0, .3), (0, -0.3)
]

FIGURE_HEIGHT = 100


def begin(fig): 
    global _figure_ref, shape_group, text_group, text_group_title, text_group_italic
    _figure_ref = fig
    shape_group = fig.g()
    text_group = fig.g(style="font-size:8;font-family:monospace;")
    text_group_title = fig.g(style="font-size:16;font-family:monospace;")
    text_group_italic = fig.g(style="font-size:8;font-family:monospace;font-style:italic;")


def add_all(parent, pos=0):
    global text_group, text_group_italic
    parent.elements.insert(pos, shape_group)
    parent.elements.insert(pos, text_group)
    parent.elements.insert(pos, text_group_title)
    parent.elements.insert(pos, text_group_italic)


def mid():
    return FIGURE_HEIGHT/2


def height():
    return FIGURE_HEIGHT


def text(text, x, y, center=False, color="black", italic=False):
    global _figure_ref, text_group, text_group_italic
    width = len(str(text))*5
    txt = _figure_ref.text(text, insert=(x - (width/2 if center else 0), y), fill=color)
    if not italic:
        text_group.add(txt)
    else:
        text_group_italic.add(txt)
    return width, 12


def title(text, x, y):
    global _figure_ref, text_group_title
    txt = _figure_ref.text(text, insert=(x, y), fill="black")
    text_group_title.add(txt)


def rect(x, y, w, h, stroke="black", fill="white"):
    global _figure_ref, shape_group
    rect = _figure_ref.rect((x,y), (w,h), stroke=stroke, fill=fill)
    shape_group.add(rect)
    return w, h


def circle(x, y, rad, stroke="black", fill="white"):
    global _figure_ref, shape_group
    rect = _figure_ref.circle((x,y), rad, stroke=stroke, fill=fill)
    shape_group.add(rect)
    return rad*2, rad*2


def line(x, y, x2, y2, stroke="black"):
    global shape_group
    ln = _figure_ref.line((x,y), (x2,y2), stroke=stroke)
    shape_group.add(ln)


def arrow(x, y, color="black"):
    global _figure_ref, shape_group, FIGURE_ARROW
    pos = (x, y)
    scaled_arrow = [(a*14, b*14) for a,b in FIGURE_ARROW]
    prev = None
    for p in scaled_arrow:
        if prev is not None:
            a = tuple(map(sum, zip(prev, pos)))
            b = tuple(map(sum, zip(p, pos)))
            shape_group.add(_figure_ref.line(a, b, stroke=color))
        prev = p
    return 1.75 * 14, 0.75 * 2 * 14
