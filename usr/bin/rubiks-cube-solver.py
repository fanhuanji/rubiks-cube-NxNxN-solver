#!/usr/bin/env python3

"""
Solve any size rubiks cube:
- For 2x2x2 and 3x3x3 just solve it
- For 4x4x4 and larger, reduce to 3x3x3 and then solve

This is a work in progress
"""

from rubikscubennnsolver import ImplementThis, SolveError, StuckInALoop, NotSolving
from rubikscubennnsolver.LookupTable import NoSteps
from math import sqrt
from pprint import pformat
from statistics import median
import argparse
import datetime as dt
import logging
import os
import resource
import sys

def remove_slices(solution):
    results = []

    for step in solution:

        if 'w' in step:
            results.append(step)

        elif step == "2U":
            results.append("Uw")
            results.append("U'")

        elif step == "2U'":
            results.append("Uw'")
            results.append("U")

        elif step == "2U2":
            results.append("Uw2")
            results.append("U2")

        elif step == "3U":
            results.append("3Uw")
            results.append("Uw'")

        elif step == "3U'":
            results.append("3Uw'")
            results.append("Uw")

        elif step == "3U2":
            results.append("3Uw2")
            results.append("Uw2")

        elif step == "2L":
            results.append("Lw")
            results.append("L'")

        elif step == "2L'":
            results.append("Lw'")
            results.append("L")

        elif step == "2L2":
            results.append("Lw2")
            results.append("L2")

        elif step == "3L":
            results.append("3Lw")
            results.append("Lw'")

        elif step == "3L'":
            results.append("3Lw'")
            results.append("Lw")

        elif step == "3L2":
            results.append("3Lw2")
            results.append("Lw2")




        elif step == "2F":
            results.append("Fw")
            results.append("F'")

        elif step == "2F'":
            results.append("Fw'")
            results.append("F")

        elif step == "2F2":
            results.append("Fw2")
            results.append("F2")

        elif step == "3F":
            results.append("3Fw")
            results.append("Fw'")

        elif step == "3F'":
            results.append("3Fw'")
            results.append("Fw")

        elif step == "3F2":
            results.append("3Fw2")
            results.append("Fw2")



        elif step == "2R":
            results.append("Rw")
            results.append("R'")

        elif step == "2R'":
            results.append("Rw'")
            results.append("R")

        elif step == "2R2":
            results.append("Rw2")
            results.append("R2")

        elif step == "3R":
            results.append("3Rw")
            results.append("Rw'")

        elif step == "3R'":
            results.append("3Rw'")
            results.append("Rw")

        elif step == "3R2":
            results.append("3Rw2")
            results.append("Rw2")



        elif step == "2B":
            results.append("Bw")
            results.append("B'")

        elif step == "2B'":
            results.append("Bw'")
            results.append("B")

        elif step == "2B2":
            results.append("Bw2")
            results.append("B2")

        elif step == "3B":
            results.append("3Bw")
            results.append("Bw'")

        elif step == "3B'":
            results.append("3Bw'")
            results.append("Bw")

        elif step == "3B2":
            results.append("3Bw2")
            results.append("Bw2")



        elif step == "2D":
            results.append("Dw")
            results.append("D'")

        elif step == "2D'":
            results.append("Dw'")
            results.append("D")

        elif step == "2D2":
            results.append("Dw2")
            results.append("D2")

        elif step == "3D":
            results.append("3Dw")
            results.append("Dw'")

        elif step == "3D'":
            results.append("3Dw'")
            results.append("Dw")

        elif step == "3D2":
            results.append("3Dw2")
            results.append("Dw2")

        else:
            results.append(step)

    return results

start_time = dt.datetime.now()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)20s %(levelname)8s: %(message)s')
log = logging.getLogger(__name__)

# Color the errors and warnings in red
logging.addLevelName(logging.ERROR, "\033[91m   %s\033[0m" % logging.getLevelName(logging.ERROR))
logging.addLevelName(logging.WARNING, "\033[91m %s\033[0m" % logging.getLevelName(logging.WARNING))


parser = argparse.ArgumentParser()
parser.add_argument('--print-steps', default=False, action='store_true', help='Display animated step-by-step solution')
parser.add_argument('--debug', default=False, action='store_true', help='set loglevel to DEBUG')
parser.add_argument('--min-memory', default=False, action='store_true', help='Load smaller tables to use less memory...takes longer to run')

# CPU mode
action = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('--colormap', default=None, type=str, help='Colors for sides U, L, etc')
parser.add_argument('--order', type=str, default='URFDLB', help='order of sides in --state, default kociemba URFDLB')
parser.add_argument('--state', type=str, help='Cube state',

# no longer used
# parser.add_argument('--test', default=False, action='store_true')

# 2x2x2
#    default='DLRRFULLDUBFDURDBFBRBLFU')
#    default='UUUURRRRFFFFDDDDLLLLBBBB')

# 3x3x3
#    default='RRBBUFBFBRLRRRFRDDURUBFBBRFLUDUDFLLFFLLLLDFBDDDUUBDLUU')
#    default='UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB') # solved

# 4x4x4
#    default='FUULURFFRLRBDDDULUDFLFBBFUURRRUBLBLBDLUBDBULDDRDFLFBBRDBFDBLRBLDULUFFRLRDLDBBRLRUFFRUBFDUDFRLFRU')
    #default='DRFDFRUFDURDDLLUFLDLLBLULFBUUFRBLBFLLUDDUFRBURBBRBDLLDURFFBBRUFUFDRFURBUDLDBDUFFBUDRRLDRBLFBRRLB') # xyzzy test cube
    default='FLDFDLBDFBLFFRRBDRFRRURBRDUBBDLURUDRRBFFBDLUBLUULUFRRFBLDDUULBDBDFLDBLUBFRFUFBDDUBFLLRFLURDULLRU') # TPR cube
#    default='UDRFFBFLFUDLBDDDRUFLBBBFBDUDBBFFUBRBBRRUBRRUFULDRFDLLDFLDUFLUFLRBRDLFDBRRUFRLBBDDULRRLLURLLUUUDF') # OLL
#    default='DRDBBBRFBBDFLDUURRRDDUUBLFRRUFUUFLFFUUFRURLFURRRLBBBDBLDFLDLDLDLFLLDUUBFDDDBBLBBLFURUFLLUFRRFBDR') # OLL
#    default='RRRRRRRLRRRLRRRFLBBFBBBBBBBBRBBBUUUUUDDDUDDDDDDULLLFLLLRLLLRLFFLBFFBLFFFLFFFBFFFDDDDUUUUUUUUUDDD')
#    default='DUFFRDLRDLBUDLBULLBLFFUBURFFURFURDUBUDLLFDLRFDLRRRDBBBDDUFULLBFFBBBBLBBRFFUDFFUDDDLLDRRBRRUURRLU') # edges take 27 steps (used to take 46 steps)
#    default='LFBDUFLDBUBBFDFBLDLFRDFRRURFDFDLULUDLBLUUDRDUDUBBFFRBDFRRRRRRRLFBLLRDLDFBUBLFBLRLURUUBLBDUFUUFBD')
#    default='DFBRULBFFUDFDRULURDUUFLLRFLFDLRRFBRFUDUFLRBDBDULRBLBBBFDUFUBUFBDLLLRURDBDBDDBBLUFDRFFULRURRRBLDL') # takes a lot of moves
#    default='UUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBB') # solved

# 5x5x5
#    default='RFFFUDUDURBFULULFDBLRLDUFDBLUBBBDDURLRDRFRUDDBFUFLFURRLDFRRRUBFUUDUFLLBLBBULDDRRUFUUUBUDFFDRFLRBBLRFDLLUUBBRFRFRLLBFRLBRRFRBDLLDDFBLRDLFBBBLBLBDUUFDDD')
#    https://www.speedsolving.com/forum/threads/arnauds-5x5x5-edge-pairing-method-examples.1447/
#    default='LDFRDDUUUUFUUUBLUUUFLDFDRFDDFBBRRRULRRRBFRRRURFRFDUBDRUBFFFUBFFFUUFFFRLDLRFDLBDDLDDDRDDDDUDDDDUULDLFBFLFFULLLRFLLLRLLLLRRBLBBRBULULBBBRUBBBRBBBBULBRFB')
#    default='UDLFDLDDLUFDUBRLBDLFLRBFRBLBBFUDURDULRRBRLFUURBUFLUBDUDRURRRBUFUFFFRUFFLDUURURFFULFFRLFDBRRFRDDBRFBBLBRDFBBBBUDDLLLDBUULUDULDLDDLBRRLRLUBBFFBDLFBDDLFR')
#    default='UUUUUUUUUUUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBBBBBBBBBBB') # solved
#    default='DFFURRULDLDLURLBDDRRBFRURFBFBFRBDLBBFRBLRFBRBBFLULDLBLULLFRUBUFLDFFLDULDDLUURRDRFBRLULUDRBDUUUBBRFFDBDFURDBBDDRULBUDRDLLLBDRFDLRDLLFDBBUFBRURFFUFFUUFU') # step10 takes 2s
#    default='URUBFUUFRDFFUUFLRDBLLBDDDLUULRDLDUBDLRBBLFLBRBFUUBBRBFFUDLFLLBFUFUDRLBFUBBURRLLRUFRDUFFDFRFUBRBBDRFRFLLFURLLFBRBLUDRDDRRDRRFDUDLFLDLUUDUDBRBBBRBDDLDFL') # step10 takes 9s
#    default='RFUBLFUBRULLUDDRLRLLFFFLUBDBLBFFUFLFURBFFLDDLFFBBRLUUDRRDLLLRDFFLBBLFURUBULBRLBDRUURDRRDFURDBUUBBFBUDRUBURBRBDLFLBDFBDULLDBBDDDRRFURLDUDUBRDFRFFDFDRLU') # step10 takes 6s, centers take 37 steps :(

# 6x6x6
#    default='FBDDDFFUDRFBBLFLLURLDLLUFBLRFDUFLBLLFBFLRRBBFDRRDUBUFRBUBRDLUBFDRLBBRLRUFLBRBDUDFFFDBLUDBBLRDFUUDLBBBRRDRUDLBLDFRUDLLFFUUBFBUUFDLRUDUDBRRBBUFFDRRRDBULRRURULFDBRRULDDRUUULBLLFDFRRFDURFFLDUUBRUFDRFUBLDFULFBFDDUDLBLLRBL')
#    default='UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUURRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB') # solved
#    defult='xxxxxxxDRRLxxLDDBxxLUUDxxFRDUxxxxxxxxxxxxxxBBLBxxURFUxxDRBDxxDFDLxxxxxxxxxxxxxxULLRxxUFLLxxBLFRxxBBRDxxxxxxxxxxxxxxLFBRxxBUUFxxFDDFxxURUFxxxxxxxxxxxxxxRFDLxxURFUxxUBBFxxRULDxxxxxxxxxxxxxxBBLFxxFLLRxxDRBBxxFDRUxxxxxxx') # good step20 IDA test

# 7x7x7
#    default='DBDBDDFBDDLUBDLFRFRBRLLDUFFDUFRBRDFDRUFDFDRDBDBULDBDBDBUFBUFFFULLFLDURRBBRRBRLFUUUDUURBRDUUURFFFLRFLRLDLBUFRLDLDFLLFBDFUFRFFUUUFURDRFULBRFURRBUDDRBDLLRLDLLDLUURFRFBUBURBRUDBDDLRBULBULUBDBBUDRBLFFBLRBURRUFULBRLFDUFDDBULBRLBUFULUDDLLDFRDRDBBFBUBBFLFFRRUFFRLRRDRULLLFRLFULBLLBBBLDFDBRBFDULLULRFDBR')

# 8x8x8
#    default='DRRRURBDDBFBRBDDBRRDUFLLURFBFLFURLFLFRBRFUBDRFDFUUBLFFFUULBBFDBDFBUBBFRFLRDLFDRBBLLFRLDFDRBURULDDRFFBFUUBLLFBRUUFDUBRDBBRDFLURUUFFUDLBRRFDUBFLRUUFFRLBFRFLRULUDFRUBBDBFFLBBDFDFLDBFRRRDDLFLBRBFBBRULDDUUBLBBURULLDDLDRUDRBUDRLUULDURLRDFLFULUFLFULRDDDUBBULRBRDFBBLFURRLULUBDDULRFBRFURBRLBRUBULBDDFBUFFBBRLRUUUFRULLBFFRFDDFFDULLDLBUDLLLLUUBBLDLLBBULULBDUDDFUBFLLDLDLFRDUDDBRRFRURRFRRLDDDDRD')

# 9x9x9
#    default='RFBLRUFLLFFLRRBDUDDBBBDUDFRUDUFFFBBFRBRDURBULFUDDFLLLDLFLRDLDBBBUUBRDBBBDFUFRUURULURBURDLFDUBFFDRDFRUBDUBRFLRRLUDLRLFBLBRRLLRDRBRBLURBLLRFRLDDFFFRBFUFURDFRRUDUFDDRRRLFLLUBBLBFDRRDLBRLUUBRDBBUBFLUUFBLLDBFFFBUFBFDBRDDDFLRFFBFFFLFRRDUUDDBUBLUUDURRBDBFFLFURDDLUBULUULULBFBRUBLLDDFLRBDBRFDUUDFURLLUBUFBLULLURDLLLBLFFRLLBLUDRLRDBLDDBRBUDRBLLRDUUUBRRFBFBBULUDUDLDRFUDDDFULRFRBDUDULBRRDBDFFRUUFRRFBDBLFBBDFURLRFDUUFRLUBURFURDDFLDFUBDFRRURRDLUDRBRBDLBFLBBRDLRDBFDUBDFFUBLFLUULLBUDLLLURDBLFFFDFLF'

# 10x10x10
#    default='ULBDLDBUFRBBBBBLBFFFDFRFBBDDFDFRFFLDLDLURRBUDRRBFLUDFRLBDURULRUUDBBBUBRURRRLDLRFFUFFFURRFBLLRRFLFUDBDRRDFULLLURFBFUUBDBBDBFLFDFUUFDUBRLUFDBLRFLUDUFBFDULDFRUBLBBBUBRRDBDDDDFURFLRDBRRLLRFUFLRDFDUULRRDULFDUDRFLBFRLDUDBDFLDBDUFULULLLBUUFDFFDBBBRBRLFLUFLFUFFRLLLFLBUDRRFDDUDLFLBRDULFLBLLULFLDLUULBUDRDFLUDDLLRBLUBBRFRRLDRDUUFLDDFUFLBDBBLBURBBRRRFUBLBRBRUBFFDBBBBLBUFBLURBLDRFLFBUDDFFRFFRLBDBDUURBUFBDFFFLFBDLDUFFBRDLBRLRLBFRUUUULRRBDBRRFDLLRRUUBDBDBFDLRDDBRUUUUUBLLURBDFUFLLRDBLRRBBLBDDBBFUDUDLDLUFDDDUURBFUFRRBLLURDDRURRURLBLDRFRUFBDRULUFFDUDLBBUURFDUDBLRRUDFRLLDULFUBFDLURFBFULFLRRRRRFDDDLFDDRUFRRLBLUBU')

# 14x14x14
#    default='FBDRLBLRRURRLDRBDLBURDFDDDRBLBBFBRDLLFDUBLFRLDFUUBFRDBFBBBULFRLBUFLBDDDLLDRBFLLBBLFBFFDFBFDDFRRRBDRRBRBDUFDRLRUDLDFDDURFLBUBBUUDLBRRDUDRDBBBLDBRBBBUFLBLRUURBDDLDRLUFFBLFRLDFBRFLDLBULFFBRLDBDDFLLRFLUBFDFBRLRLFDBLBURLBLFRFBLLDULUDURLBUUULLRRLUBDDLURLLRFURFRFRBDDUBLDFBLUDRLRDRRBLFUFRDUFFRULBLRBBRUFDBUBBBBLDBRBLDDRRFDDBFFUUBRBLFUBBRFUURBFDRLURLRBFUUFUBRUDRBDFBBFURFLFFDRDFUFFULFLUBDFUFFDLRRFRUDUDLBBBDLLLDUFUDRFDBLRRFFLRUFDRFURDLRRDRDLFBRLRLULRFBDLFDRLFRDDFLLDBFBUBBRLLDLFURFRFULUBLUBFLFFBFDFBDUUBURUUUBFUBDLLFLUUUFDUDLUUULDLLUDDBUFRDRULRLLULRULFBLUDFURFLFUBDLLFLFUBUUBBUFLUDUBRDBLFFUUUFDRLRULUDDRLRBLRUUFBRRRRULBDLFBFLDLRDFUBLUBRDDFUULFLDLUBFURRURUBDFFFDLRFFLBRFRDRUDUULURULLDFRBUDRDLFUFULDBLUBFRFBURDLLUUFDURLRDBLFFRFDBFURLFUBLUUUFFRULUBURRURFDDBFUFRBURBBDRFUDDFDLRUURFBBDBDRLUBRRBFDFRDFDLRDUFFUBRRBDBBLDLFDUDDRLFRRRBUUUBRFUFBUFFBRRDRDDBBDRUULDRFRFBUFLFFBLRBFLLLRUDFDRUDLDRLFRLUFLUBRDUFDDLLUDDRBUBBBDRDBBFRBDDRRLRRUUBBUDUDBLDBDFLFRFUBFLFDBBLRLULDBRFBRRLUUURDFFFDBLDUDBRFDDFFUBLUUURBBULFUFUDFBRDLLFURBULULBUDLUFFBDRBRRDBUUULFDURRDFDDLUDBDRBFBUFLULURUFDRFRFBBFBBBDRLBLUDLDRDLLDRRLLDLFBRBRLDUFBDDUDBLDFRFBBBDRDRDDLDRULFFLLFLBLDFLURLBUDFBDLRBLFDFLUDDFUBUBLURBBBLFRLFLBDDBURFFBFRRL')

# 15x15x15
#    default='RLURLURBDDULFUUURFLRBLURUBFDBULFLUBBFLDUFBDRFRBRUDFULFRUFLUDFRLFDFLLFDBULURRLBFBUURDULFDFBLRRRLFULLFFFDUULRRRUUUUFDBLDDFFLRDLLUURUBBULUFFURBRRLBBUUBBFDRRBRBRLUDLUDRBFBFULLRRBBFBFRDDDLDDDFRFUFLURUFLBDLUBRLDFRRDBDBFLFUDFLDFFURLFULLDDRURRDLRFLDFLULUUDDRFDRBLRBRBFUFDBDUUDBRRBDFBLBLRBBLBFLLDUBFFFFBDDRLBBBRFDFFUBBDURFLUUDDDRDDLDBRLBULLFLFBRBRBLUDDLRDRDUDFLFRUFLDLBLURDDDRUFDLBRDRLFBDBLDRFBFFBURULUDRRBRDFRFFLULLUBRDRRRDUFRBLFULUBBUFFBRBBFRLFDRRDBLDFRDRDDRLRUULBDURDURFDDLFDUUDBFLBDUFBULFRRDUDUBFBUDBBFUDFUUDLUDDRFDDDFRRRBUDRBFBBULLUFBLRLFLLBRRRRUBDRFLFDFDBLRFLURULULFFBUUUUFDBBLDLUBBRUBBBRBFLULLBLUUULLUBFFDULDFFBFFFUFFDUDRFBUFLDDLURFLRFLRFBUUBLRFDDRULUUUFFRDDBLRDULFURUDDBDLBBUUBFURFRFBRLBUULBLDDDBUBRFFULLUDFFDLDFUBLLBLDFFDDLBDUFUFFLBBBUBULDDFBRRFFLDUDDFRBLRRDDUDLBDBLURBUDBRRLUBBDRFBUFRDRDRBBDULBUFFDRBBDFBUULFFRLLDURRRDFFUUFULDULURLDLUUUDLBBUDLDRFBDBBDLUFBRRFDFLLDLFDBRBBRFUDDDBURDRBUBRUBDUBLDLLDLURLDFDBRUBDLDFRRRBRLULFRFLDRLBUBRUBLFBFDFFLFRFDFLBRULLRBLDRBBFURRRDUUULLULLDLBLBBDFBUUUBRRUFFBRUDBFRDFDLFLFFRFFFFRULDFFDFRUBBBRURBUFLBDFBBBBBRRRLFLFBDRRUFLURDDLRRBRLLFURRURBRFLLLFFURBFULFRFFBLDUUUUBDDUFFDRBRLDDFRBULDDDFFRURUFLDRFLDFBLRUFFUBBDFFDBLLDBDUBDLDLUDFBFLRULRRBDBLRBLDLUURRLLRULDBLBLLRRFDDRBBRBUBDDULDRFBFBBFLUFBLUULDDFDBRLLUBUBBDFBBLBBUBLULDRUDBLRULDUDLUFRRDLLUDDBUFLFLBUFUURFDRDLBURLLRRRULRBFFRRBRFBUBRBUUFRLRDRDLBBRFLLLDDBRFUFRBULFLFDRDDRRDBF')

args = parser.parse_args()

if args.debug:
    log.setLevel(logging.DEBUG)

# no longer used
#if args.test:
#    cube = RubiksCube444(solved_444, args.order, args.colormap, avoid_pll=True, debug=args.debug)
#    cube.test()
#    sys.exit(0)

try:
    size = int(sqrt((len(args.state) / 6)))

    if size == 2:
        from rubikscubennnsolver.RubiksCube222 import RubiksCube222
        cube = RubiksCube222(args.state, args.order, args.colormap, args.debug)
    elif size == 3:
        from rubikscubennnsolver.RubiksCube333 import RubiksCube333
        cube = RubiksCube333(args.state, args.order, args.colormap, args.debug)
    elif size == 4:
        from rubikscubennnsolver.RubiksCube444 import RubiksCube444, solved_444
        cube = RubiksCube444(args.state, args.order, args.colormap, avoid_pll=True, debug=args.debug)
    elif size == 5:
        use_tsai = False

        if use_tsai
            from rubikscubennnsolver.RubiksCube555 import RubiksCubeTsai555, solved_555
            cube = RubiksCubeTsai555(args.state, args.order, args.colormap, args.debug)
        else:
            from rubikscubennnsolver.RubiksCube555 import RubiksCube555, solved_555
            cube = RubiksCube555(args.state, args.order, args.colormap, args.debug)
    elif size == 6:
        from rubikscubennnsolver.RubiksCube666 import RubiksCube666
        cube = RubiksCube666(args.state, args.order, args.colormap, args.debug)
    elif size == 7:
        from rubikscubennnsolver.RubiksCube777 import RubiksCube777
        cube = RubiksCube777(args.state, args.order, args.colormap, args.debug)
    elif size % 2 == 0:
        from rubikscubennnsolver.RubiksCubeNNNEven import RubiksCubeNNNEven
        cube = RubiksCubeNNNEven(args.state, args.order, args.colormap, args.debug)
    else:
        from rubikscubennnsolver.RubiksCubeNNNOdd import RubiksCubeNNNOdd
        cube = RubiksCubeNNNOdd(args.state, args.order, args.colormap, args.debug)

    # TPR cube FLDFDLBDFBLFFRRBDRFRRURBRDUBBDLURUDRRBFFBDLUBLUULUFRRFBLDDUULBDBDFLDBLUBFRFUFBDDUBFLLRFLURDULLRU for
    # https://alg.cubing.net/?puzzle=4x4x4&alg=B_Fw-_L-_Uw_R2_B_Fw-_Uw_%2F%2F_end_of_phase1_(8%2F8_moves)%0AB_Fw_D-_R_F__%2F%2F_end_of_phase_2_(5%2F13_moves)%0ARw2_D_Fw2_U_R2_Fw2_Uw2_Fw2_D-_U2_Fw2_%2F%2Fend_of_phase3_(11%2F24_moves)&setup=B_D-_R2-_D_B2-_L2-_U_R2-_D_F2-_L2-_B_L_B-_R_B-_R2-_U_F2-_L_Uw2-_Rw2-_R_Uw2-_B_U2-_R-_Uw2-_B_R-_Fw2-_F_B_R_Uw-_R2-_B-_Rw2-_Uw_Rw-_Uw-_L_Fw_R_B-_Rw2-&view=playback

    # Uncomment to produce a cube from alg.cubing.net
    # https://alg.cubing.net/?alg=R_Rw-_D_Uw_R2_Fw2_Uw2_F2_Uw_Fw_%2F%2F_stage_centres%0AU_L_Fw2_D2_L_Fw2_U_Rw2_U-_%2F%2F_3_dedges_%26%232b%3B_partial_centres%0AB_D-_B-_Uw2_L_U-_F_R_Fw2_%2F%2F_6_dedges_%26%232b%3B_centres%0ARw2_U_R-_U-_D-_L2_D_Rw2_%2F%2F_9_dedges%0AFw2_D-_F-_D_Fw2_%2F%2F_12_dedges%0AL2_U-_D_R2_L-_B2_D-_F_%2F%2F_Kociemba_phase_1%0AR2_F2_U2_R2_L2_F2_U-_R2_U-_L2_U2_R2_B2_%2F%2F_Kociemba_phase_2&puzzle=4x4x4&setup=(R1_Rw3_D1_Uw1_R2_Fw2_Uw2_F2_Uw1_Fw1_U1_L1_Fw2_D2_L1_Fw2_U1_Rw2_U3_B1_D3_B3_Uw2_L1_U3_F1_R1_Fw2_Rw2_U1_R3_U3_D3_L2_D1_Rw2_Fw2_D3_F3_D1_Fw2_L2_U3_D1_R2_L3_B2_D3_F1_R2_F2_U2_R2_L2_F2_U3_R2_U3_L2_U2_R2_B2_x-_z-)-&view=playback
    '''
    cube = RubiksCube444(solved_444, args.order, args.colormap)
    for step in remove_slices("B D' R2' D B2' L2' U R2' D F2' L2' B L B' R B' R2' U F2' L Uw2' Rw2' R Uw2' B U2' R' Uw2' B R' Fw2' F B R Uw' R2' B' Rw2' Uw Rw' Uw' L Fw R B' Rw2'".split()):
        cube.rotate(step)

    kociemba_string = cube.get_kociemba_string(True)
    print(kociemba_string)
    cube.print_cube()
    sys.exit(0)

    # compress a solution
    cube = RubiksCube555(solved_555, args.order, args.colormap)
    cube.solution = "Rw' Lw x F2 Rw Lw' x' F' Uw Dw' y' B' Uw Dw' y' B Uw Dw' y' B Uw Dw' y' B' Uw Dw' y' F'".split()
    cube.compress_solution()
    cube.print_solution()
    sys.exit(0)

    # run build_tsai_phase2_orient_edges_555
    cube = RubiksCube555(solved_555, args.order, args.colormap)
    cube.build_tsai_phase3_orient_edges_555()
    sys.exit(0)
    '''

    # print cube rotations
    '''
    cube = RubiksCube444(solved_444, args.order, args.colormap)
    original_state = cube.state[:]
    rotations = (
                (),
                ("y",),
                ("y'",),
                ("y", "y"),
                ("x", "x", "y"),
                ("x", "x", "y'"),
                ("x", "x", "y", "y"),
                ("y'", "x", "y"),
                ("y'", "x", "y'"),
                ("y'", "x", "y", "y"),
                ("x", "y"),
                ("x", "y'"),
                ("x", "y", "y"),
                ("y", "x", "y"),
                ("y", "x", "y'"),
                ("y", "x", "y", "y"),
                ("x'", "y"),
                ("x'", "y'"),
                ("x'", "y", "y")
    )

    for rotation_seq in rotations:
        cube.state = original_state[:]

        for step in rotation_seq:
            cube.rotate(step)

        result = []
        for side in (cube.sideU, cube.sideL, cube.sideF, cube.sideR, cube.sideB, cube.sideD):
            result.append(cube.state[side.center_pos[0]])
        print(''.join(result))

    sys.exit(0)
    '''

    cube.min_memory = args.min_memory
    cube.sanity_check()
    cube.print_cube()
    cube.www_header()
    cube.www_write_cube("Initial Cube")

    try:
        cube.solve()
    except NotSolving:
        if cube.heuristic_stats:
            log.info("%s: heuristic_stats raw\n%s\n\n" % (cube, pformat(cube.heuristic_stats)))

            for (key, value) in cube.heuristic_stats.items():
                cube.heuristic_stats[key] = int(median(value))

            log.info("%s: heuristic_stats median\n%s\n\n" % (cube, pformat(cube.heuristic_stats)))
            sys.exit(0)
        else:
            raise

    end_time = dt.datetime.now()
    log.info("Final Cube")
    cube.print_cube()
    cube.print_solution()

    log.info("***********************************************************")
    log.info("See /tmp/solution.html for more detailed solve instructions")
    log.info("***********************************************************\n")

    # Now put the cube back in its initial state and verify the solution solves it
    solution = cube.solution
    cube.re_init()
    len_steps = len(solution)

    for (i, step) in enumerate(solution):

        if args.print_steps:
            print(("Phase     : %s" % cube.phase()))
            print(("Move %d/%d: %s" % (i+1, len_steps, step)))

        cube.rotate(step)

        www_desc = "Phase: %s<br>\nCube After Move %d/%d: %s<br>\n" % (cube.phase(), i+1, len_steps, step)
        cube.www_write_cube(www_desc)

        if args.print_steps:
            cube.print_cube()
            print("\n\n\n\n")

    cube.www_footer()

    if args.print_steps:
        cube.print_cube()

    print("\nMemory : {:,} bytes".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    print("Time   : %s" % (end_time - start_time))
    print("")

    if not cube.solved():
        kociemba_string = cube.get_kociemba_string(False)
        edge_swap_count = cube.get_edge_swap_count(edges_paired=True, orbit=None, debug=True)
        corner_swap_count = cube.get_corner_swap_count(debug=True)

        raise SolveError("cube should be solved but is not, edge parity %d, corner parity %d, kociemba %s" %
            (edge_swap_count, corner_swap_count, kociemba_string))

except (ImplementThis, SolveError, StuckInALoop, NoSteps, KeyError):
    cube.print_cube_layout()
    cube.print_cube()
    cube.print_solution()
    print((cube.get_kociemba_string(True)))
    raise
