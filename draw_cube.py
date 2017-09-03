import itertools

from cube import U, L, F, R, D, B, BLUE, ORANGE, WHITE, RED, GREEN, YELLOW, get_pos

cube_color = {BLUE: color(0, 0, 255),
              ORANGE: color(255, 123, 0),
              WHITE: color(255),
              RED: color(255, 0, 0),
              GREEN: color(0, 255, 0),
              YELLOW: color(255, 255, 0)}

cubie_positions = [((0, 0), (0, 0, 1, 0)),
                   ((1, 0), (0, 0, 1, 1)),
                   ((2, 0), (0, 0, 0, 1)),
                   ((2, 1), (1, 0, 0, 1)),
                   ((2, 2), (1, 0, 0, 0)),
                   ((1, 2), (1, 1, 0, 0)),
                   ((0, 2), (0, 1, 0, 0)),
                   ((0, 1), (0, 1, 1, 0)),
                   ((1, 1), (1, 1, 1, 1))]

def draw_face(base, face, cu, pos_xrange):
    f_base = float(base) / 3.0
    for cpos, pos in enumerate(itertools.chain((i % 8 for i in pos_xrange), [8])):
        (x, y), corners = cubie_positions[pos]
        fill(cube_color[cu.squares[get_pos(face, cpos)]])
        rect(x * f_base, y * f_base, f_base, f_base,
             *(base * 0.1 * i for i in corners))

def draw_cube(base, cu):
    pushMatrix()
    translate(*([-base * 0.5] * 3))

    pushMatrix()
    fill(255)
    draw_face(base, D, cu, reversed(xrange(7, 15)))
    translate(0, 0, base)
    fill(255, 255, 0)
    draw_face(base, U, cu, xrange(8))
    popMatrix()

    pushMatrix()
    fill(255, 0, 0)
    rotateY(HALF_PI)
    scale(-1, 1)
    draw_face(base, L, cu, xrange(2, 10))
    translate(0, 0, base)
    fill(255, 123, 0)
    draw_face(base, R, cu, reversed(xrange(5, 13)))
    popMatrix()

    pushMatrix()
    fill(0, 0, 255)
    rotateX(HALF_PI)
    draw_face(base, B, cu, xrange(8))
    translate(0, 0, -base)
    fill(0, 255, 0)
    draw_face(base, F, cu, reversed(xrange(7, 15)))
    popMatrix()

    popMatrix()