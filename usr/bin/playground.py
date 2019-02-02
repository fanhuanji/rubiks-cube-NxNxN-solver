#!/usr/bin/env python3

from pprint import pformat, pprint
from rubikscubennnsolver import wing_strs_all, reverse_steps
from rubikscubennnsolver.LookupTable import steps_on_same_face_and_layer
from rubikscubennnsolver.misc import parse_ascii_777
from rubikscubennnsolver.RubiksCube777 import RubiksCube777
from rubikscubennnsolver.RubiksCube444 import RubiksCube444, solved_444
from rubikscubennnsolver.RubiksCube555 import RubiksCube555, solved_555, edges_partner_555, edges_recolor_pattern_555, wings_for_edges_pattern_555
from rubikscubennnsolver.RubiksCube555ForNNN import RubiksCube555ForNNN
from rubikscubennnsolver.RubiksCube666 import RubiksCube666, moves_666, solved_666, rotate_666
import itertools
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)20s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))

# Build wing_str_combos_two and wing_str_combos_four
#pprint(tuple(itertools.combinations(wing_strs_all, 2)))
#pprint(tuple(itertools.combinations(wing_strs_all, 4)))

'''
ed_state = """WYWYYWWWWWWWWWWWWWWWWWWWWRRRRRRRRRRRRRRRRRRRRBBRBBGGGGGGGGGGGGGGGGGGGGBBGBOYYYYWYYYYWYYYYYYYYYWYYYYYBOOOOOOOOOOOOOOOOOOOGRORRGGBGRBBBBBBBBBBBBBBBOOBOO"""
ed_state = ed_state.replace("W", "U")
ed_state = ed_state.replace("O", "L")
ed_state = ed_state.replace("G", "F")
ed_state = ed_state.replace("R", "R")
ed_state = ed_state.replace("B", "B")
ed_state = ed_state.replace("Y", "D")
'''

#cube = RubiksCube555(solved_555, "URFDLB")
cube = RubiksCube555ForNNN(solved_555, "URFDLB")
cube.cpu_mode = "fast"
cube.rotate("z'")

for step in reverse_steps("D' F2 Rw Uw2 Lw' Fw2 Uw' F2 L Uw' Lw R2 Uw Rw' Fw2 Rw Fw2 R Uw' Dw2 U2 Bw' Fw' R' B' D2 Fw' L2 Uw2 R' Fw D' Fw2 Bw R Fw Bw' L2 D Rw Dw2 F U F' Dw2 U' Rw' Uw2 Lw' L F L' F' Lw Uw2 U F Uw2 F L' D L F' Uw2 R' L B2 U D F2 D' F' B2 D' L2 R2 B L' D2 L2 R' U".split()):
    cube.rotate(step)
cube.print_cube()

for step in "D' F2 Rw Uw2 Lw' Fw2 Uw' F2 L Uw' Lw R2 Uw Rw' Fw2 Rw Fw2 R Uw' Dw2 U2 Bw' Fw' R' B' D2 Fw' L2 Uw2 R' Fw D' Fw2 Bw R Fw Bw' ".split():
    cube.rotate(step)

cube.solution = []
cube.print_cube()
#sys.exit(0)

cube.solve()
cube.print_solution(True)
