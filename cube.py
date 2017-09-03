import sys
import re
import argparse
import itertools

from copy import deepcopy

"""
Program defining a rubik's cube and a number of transformations through a
series of abstractions on it
"""

DEFAULT_CUBE = sum(([i for _ in range(8)] for i in range(6)), []) + list(range(6))

#global constants for colours. These are ordered to follow the faces
BLUE, ORANGE, WHITE, RED, GREEN, YELLOW = range(6)
NUM_TO_COL = ["BLUE", "ORANGE", "WHITE", "RED", "GREEN", "YELLOW"]
COL_TO_NUM = dict((i, ind) for ind, i in enumerate(NUM_TO_COL))

#global constants for faces. These are top to bottom left to right as in cube_template
U, L, F, R, D, B = range(6)
FACE_TO_NUM = dict(zip("ULFRDB", range(6)))
NUM_TO_FACE = list("ULFRDB")

#for invalid positions
class PositionException(Exception):
    pass

#transform a face and face index to a lower level cube index
def get_pos(face, index):
    if index == 8:
        return 6 * 8 + face
    elif index >= 0:
        return face * 8 + index

    else:
        raise PositionException("{}, {}".format(face, index))

#convert a number to a position, as a string
def to_pos(n):
    quot, rem = divmod(n, 8)
    if quot == 6:
        return "MID{}".format(NUM_TO_FACE[rem])
    else:
        return "{}{}".format(NUM_TO_FACE[quot], rem)

#cube class
class Cube:
    #squares as a contiguous list
    def __init__(self):
        self.squares = DEFAULT_CUBE

    #apply a transformation to the cube
    def transform(self, mapping):
        lookup = -mapping
        self.squares = [self.squares[lookup[i]] for i in range(len(self.squares))]

    #cube as a string
    def __str__(self):
        return CUBE_TEMP.format(*(NUM_TO_COL[i][0] for ind, i in enumerate(self.squares)))

#merge dicts - b overrides a
def merge_dicts(a, b):
    return [i if b[ind] == ind else b[ind] for ind, i in enumerate(a)]

#chains dictionaries - should be entire bijections
def chain_dicts(a, b):
    return [b[i] for i in a]

#inverts a dict
def invert(d):
    x = [None for _ in range(54)]
    for b, a in enumerate(d):
        x[a] = b
    return x

#mapping of face squares to squares, this is a step of abstraction in building a full cube transformation
class Mapping:
    #mapping directly from a list
    def __init__(self, l=list(range(54))):
        self.map = deepcopy(l)

    #from dictionary
    @classmethod
    def from_dict(cls, d):
        m = cls()
        for a, b in d.items():
            m.map[a] = b
        return m

    #maps two sequences of cube positions
    @classmethod
    def from_seqs(cls, start, end):
        return cls.from_dict(dict(zip(start, end)))

    #mapping from tuples
    @classmethod
    def from_tuples(cls, t):
        return cls.from_dict(dict(t))

    #allows quick indexing of a map
    __getitem__ = lambda self, *args: self.map.__getitem__(*args)

    #merge mappings, put on binary addition
    def __add__(self, other):
        return Mapping(merge_dicts(self.map, other.map))

    #chain mappings (as if doing two consecutive moves), put on bitwise or
    def __or__(self, other):
        return Mapping(chain_dicts(self.map, other.map))

    #invert mapping, put on binary negation
    def __neg__(self):
        return Mapping(invert(self.map))

    #syntactic sugar enabling the binary subtraction operator
    def __sub__(self, other):
        return self + (-other)

    #mapping as str (shows inner list)
    def __str__(self):
        return "Mapping<{}>".format(", ".join("{}: {}".format(to_pos(a), to_pos(b)) for a, b in enumerate(self.map)))

    #mapping as str - shortened version
    def short_str(self):
        return "Mapping<{}>".format(", ".join("{}: {}".format(to_pos(a), to_pos(b)) for a, b in enumerate(self.map) if a != b))

#a circular chain between consecutive map tuples tuples in a list
#could potentially have been done in one line but would be unbelievably complicated
#maps: List[Tuple[int(face), List[int...(cube squares)]]]
def circular_chain(maps):
    out = Mapping()
    for ind, i in enumerate(maps):
        FACE, seq = i
        FACE2, seq2 = maps[(ind + 1) % len(maps)]
        out += Mapping.from_seqs([get_pos(FACE, j) for j in seq],
                                 [get_pos(FACE2, j) for j in seq2])
    return out

#a mapping to rotate one face.
def turn_face(X):
    return Mapping.from_tuples((get_pos(X, i), get_pos(X, (i + 2) % 8)) for i in range(8))

#maps face X onto face Y
#helpermap map_face(X, Y) = (X[*] -> Y[n] ->),
#                           (X[8] -> Y[8] ->);
def map_face(X, Y):
    return Mapping.from_tuples((get_pos(X, i), get_pos(Y, i)) for i in range(9))

#turns cube up - face F becomes U, and B becomes F
turn_up = (map_face(F, U)
         + map_face(U, B)
         + map_face(B, D)
         + map_face(D, F)
         + turn_face(R)
         - turn_face(L))

turn_down = -turn_up

#turns cube right - F becomes R, and L becomes F
turn_right = (map_face(F, R)
            + (map_face(R, B) | (turn_face(B) | turn_face(B)))
            + (map_face(B, L) | (turn_face(L) | turn_face(L)))
            + map_face(L, F)
            + turn_face(D)
            - turn_face(U))

turn_left = -turn_right

#turn the front face of the cube
turn_front = (turn_face(F)
            + circular_chain([(U, [6, 5, 4]),
                              (R, [0, 7, 6]),
                              (D, [2, 1, 0]),
                              (L, [4, 3, 2])]))

turn_cube = turn_down | turn_right | turn_up

#the set of final moves as Mappings
_finalmoves_as_int = {F: turn_front,
                      B: turn_up | turn_up | turn_front | turn_up | turn_up,
                      D: turn_up | turn_front | turn_down,
                      U: turn_down | turn_front | turn_up,
                      L: turn_right | turn_front | turn_left,
                      R: turn_left | turn_front | turn_right}

FINALMOVES_AS_INT = [_finalmoves_as_int[i] for i in range(6)]

#set of final primitive moves as Mappings
FINALMOVES = {NUM_TO_FACE[a]: b for a, b in enumerate(FINALMOVES_AS_INT)}

#the set of final turns as Mappings
FINALTURNS = {"X": turn_up,
              "X'": turn_down,
              "Y'": turn_right,
              "Y": turn_left,
              "Z": turn_cube,
              "Z'": -turn_cube}

_inverse_moves = {"{}'".format(a): -b for a, b in FINALMOVES.items()}

FINALMAPPINGS = dict(itertools.chain(FINALMOVES.items(), _inverse_moves.items(), FINALTURNS.items()))