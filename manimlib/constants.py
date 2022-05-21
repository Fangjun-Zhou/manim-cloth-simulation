import numpy as np


# Sizes relevant to default camera frame
ASPECT_RATIO = 16.0 / 9.0
FRAME_HEIGHT = 8.0
FRAME_WIDTH = FRAME_HEIGHT * ASPECT_RATIO
FRAME_Y_RADIUS = FRAME_HEIGHT / 2
FRAME_X_RADIUS = FRAME_WIDTH / 2

DEFAULT_PIXEL_HEIGHT = 1080
DEFAULT_PIXEL_WIDTH = 1920
DEFAULT_FRAME_RATE = 30

SMALL_BUFF = 0.1
MED_SMALL_BUFF = 0.25
MED_LARGE_BUFF = 0.5
LARGE_BUFF = 1

DEFAULT_MOBJECT_TO_EDGE_BUFFER = MED_LARGE_BUFF
DEFAULT_MOBJECT_TO_MOBJECT_BUFFER = MED_SMALL_BUFF


# All in seconds
DEFAULT_POINTWISE_FUNCTION_RUN_TIME = 3.0
DEFAULT_WAIT_TIME = 1.0


ORIGIN = np.array((0., 0., 0.))
UP = np.array((0., 1., 0.))
DOWN = np.array((0., -1., 0.))
RIGHT = np.array((1., 0., 0.))
LEFT = np.array((-1., 0., 0.))
IN = np.array((0., 0., -1.))
OUT = np.array((0., 0., 1.))
X_AXIS = np.array((1., 0., 0.))
Y_AXIS = np.array((0., 1., 0.))
Z_AXIS = np.array((0., 0., 1.))

# Useful abbreviations for diagonals
UL = UP + LEFT
UR = UP + RIGHT
DL = DOWN + LEFT
DR = DOWN + RIGHT

TOP = FRAME_Y_RADIUS * UP
BOTTOM = FRAME_Y_RADIUS * DOWN
LEFT_SIDE = FRAME_X_RADIUS * LEFT
RIGHT_SIDE = FRAME_X_RADIUS * RIGHT

PI = np.pi
TAU = 2 * PI
DEGREES = TAU / 360
# Nice to have a constant for readability
# when juxtaposed with expressions like 30 * DEGREES
RADIANS = 1

FFMPEG_BIN = "ffmpeg"

JOINT_TYPE_MAP = {
    "auto": 0,
    "round": 1,
    "bevel": 2,
    "miter": 3,
}

# Related to Tex
PRESET_PREAMBLE = {
    "default": (
        "\\usepackage[english]{babel}",
        "\\usepackage[utf8]{inputenc}",
        "\\usepackage[T1]{fontenc}",
        "\\usepackage{amsmath}",
        "\\usepackage{amssymb}",
        "\\usepackage{dsfont}",
        "\\usepackage{setspace}",
        "\\usepackage{tipa}",
        "\\usepackage{relsize}",
        "\\usepackage{textcomp}",
        "\\usepackage{mathrsfs}",
        "\\usepackage{calligra}",
        "\\usepackage{wasysym}",
        "\\usepackage{ragged2e}",
        "\\usepackage{physics}",
        "\\usepackage{xcolor}",
        "\\usepackage{microtype}",
        "\\usepackage{pifont}",
        "\\DisableLigatures{encoding = *, family = * }",
        "\\linespread{1}",
    ),
    "ctex": (
        "\\usepackage[UTF8]{ctex}",
        "\\usepackage[english]{babel}",
        "\\usepackage{amsmath}",
        "\\usepackage{amssymb}",
        "\\usepackage{dsfont}",
        "\\usepackage{setspace}",
        "\\usepackage{tipa}",
        "\\usepackage{relsize}",
        "\\usepackage{textcomp}",
        "\\usepackage{mathrsfs}",
        "\\usepackage{calligra}",
        "\\usepackage{wasysym}",
        "\\usepackage{ragged2e}",
        "\\usepackage{physics}",
        "\\usepackage{xcolor}",
        "\\usepackage{microtype}",
        "\\linespread{1}",
    ),
    "minimized": (
        "\\usepackage{amsmath}",
        "\\usepackage{amssymb}",
        "\\usepackage{xcolor}",
    ),
}

# Related to Text
NORMAL = "NORMAL"
ITALIC = "ITALIC"
OBLIQUE = "OBLIQUE"
BOLD = "BOLD"

DEFAULT_STROKE_WIDTH = 4

# For keyboard interactions
CTRL_SYMBOL = 65508
SHIFT_SYMBOL = 65505
COMMAND_SYMBOL = 65517
DELETE_SYMBOL = 65288
ARROW_SYMBOLS = list(range(65361, 65365))

SHIFT_MODIFIER = 1
CTRL_MODIFIER = 2
COMMAND_MODIFIER = 64

# Colors
BLUE_E = "#1C758A"
BLUE_D = "#29ABCA"
BLUE_C = "#58C4DD"
BLUE_B = "#9CDCEB"
BLUE_A = "#C7E9F1"
TEAL_E = "#49A88F"
TEAL_D = "#55C1A7"
TEAL_C = "#5CD0B3"
TEAL_B = "#76DDC0"
TEAL_A = "#ACEAD7"
GREEN_E = "#699C52"
GREEN_D = "#77B05D"
GREEN_C = "#83C167"
GREEN_B = "#A6CF8C"
GREEN_A = "#C9E2AE"
YELLOW_E = "#E8C11C"
YELLOW_D = "#F4D345"
YELLOW_C = "#FFFF00"
YELLOW_B = "#FFEA94"
YELLOW_A = "#FFF1B6"
GOLD_E = "#C78D46"
GOLD_D = "#E1A158"
GOLD_C = "#F0AC5F"
GOLD_B = "#F9B775"
GOLD_A = "#F7C797"
RED_E = "#CF5044"
RED_D = "#E65A4C"
RED_C = "#FC6255"
RED_B = "#FF8080"
RED_A = "#F7A1A3"
MAROON_E = "#94424F"
MAROON_D = "#A24D61"
MAROON_C = "#C55F73"
MAROON_B = "#EC92AB"
MAROON_A = "#ECABC1"
PURPLE_E = "#644172"
PURPLE_D = "#715582"
PURPLE_C = "#9A72AC"
PURPLE_B = "#B189C6"
PURPLE_A = "#CAA3E8"
GREY_E = "#222222"
GREY_D = "#444444"
GREY_C = "#888888"
GREY_B = "#BBBBBB"
GREY_A = "#DDDDDD"
WHITE = "#FFFFFF"
BLACK = "#000000"
GREY_BROWN = "#736357"
DARK_BROWN = "#8B4513"
LIGHT_BROWN = "#CD853F"
PINK = "#D147BD"
LIGHT_PINK = "#DC75CD"
GREEN_SCREEN = "#00FF00"
ORANGE = "#FF862F"

MANIM_COLORS = [
    BLACK, GREY_E, GREY_D, GREY_C, GREY_B, GREY_A, WHITE,
    BLUE_E, BLUE_D, BLUE_C, BLUE_B, BLUE_A,
    TEAL_E, TEAL_D, TEAL_C, TEAL_B, TEAL_A,
    GREEN_E, GREEN_D, GREEN_C, GREEN_B, GREEN_A,
    YELLOW_E, YELLOW_D, YELLOW_C, YELLOW_B, YELLOW_A,
    GOLD_E, GOLD_D, GOLD_C, GOLD_B, GOLD_A,
    RED_E, RED_D, RED_C, RED_B, RED_A,
    MAROON_E, MAROON_D, MAROON_C, MAROON_B, MAROON_A,
    PURPLE_E, PURPLE_D, PURPLE_C, PURPLE_B, PURPLE_A,
    GREY_BROWN, DARK_BROWN, LIGHT_BROWN,
    PINK, LIGHT_PINK,
]

# Abbreviated names for the "median" colors
BLUE = BLUE_C
TEAL = TEAL_C
GREEN = GREEN_C
YELLOW = YELLOW_C
GOLD = GOLD_C
RED = RED_C
MAROON = MAROON_C
PURPLE = PURPLE_C
GREY = GREY_C

COLORMAP_3B1B = [BLUE_E, GREEN, YELLOW, RED]
