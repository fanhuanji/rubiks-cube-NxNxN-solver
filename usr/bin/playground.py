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

cube = RubiksCube555ForNNN(solved_555, "URFDLB")
cube.cpu_mode = "fast"

for step in "Rw2 B2 U2 Lw U2 Rw' U2 Rw U2 F2 Rw F2 Lw' B2 Rw2".split():
    cube.rotate(step)

cube.print_cube()
#cube.edges_flip_to_original_orientation()

#state = edges_recolor_pattern_555(cube.state[:])
#edges_state = ''.join([state[index] for index in wings_for_edges_pattern_555])
#print(edges_state)


cube.solve()
cube.print_solution(True)
