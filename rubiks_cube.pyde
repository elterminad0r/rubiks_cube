from draw_cube import draw_cube
from cube import Cube, FINALMAPPINGS
import random as random_

o1 = ord('1')
o2 = ord('2')
o3 = ord('3')
os = ord('S')
oa = ord('A')
o_ = ord(' ')

def random_move():
    cu.transform(random_.choice(pool))

pool = list(FINALMAPPINGS.values())

ks = {i: False for i in range(256)}
ord_ = {chr(i) : i for i in range(256)}

moves = dict(zip("udlrfbxyz", map(FINALMAPPINGS.__getitem__, "UDLRFBXYZ")))
for k, v in moves.items():
    moves[k.upper()] = -v

def setup():
    global xo, yo, zo, cu, do_stroke
    size(800, 800, P3D)
    xo = QUARTER_PI
    yo = 0
    zo = QUARTER_PI
    cu = Cube()
    do_stroke = True

def draw():
    global xo, yo, zo
    if ks[os]:
        random_move()
    background(0)
    stroke(0)
    xo += 0.01 * ks[o1] * (-2 * ks[SHIFT] + 1)
    yo += 0.01 * ks[o2] * (-2 * ks[SHIFT] + 1)
    zo += 0.01 * ks[o3] * (-2 * ks[SHIFT] + 1)
    translate(400, 400, 400)
    rotateX(xo)
    rotateY(yo)
    rotateZ(zo)
    draw_cube(100, cu)
    fill(0)
    box(99)

def keyPressed():
    global do_stroke
    ks[       keyCode] = True
    
    if key in moves:
        cu.transform(moves[key])
    
    if keyCode == o_:
        setup()
    elif keyCode == oa:
        random_move()
        

def keyReleased():
    ks[keyCode] = False
