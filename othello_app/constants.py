from collections import namedtuple


TITLE = "Othello App"
WINDOW_SIZE = "360x340"
FONT = ""
FONT_SIZES = {
    "m": 16,
    "l": 24
}
PLACEABLE_TXT = "・"
GAME_OVER_MSG = "GAME OVER!"
PASS_BTN_MSG = "Pass"

SIDE_LEN = 8
EMPTY, BLACK, WHITE = 0, 1, -1
DISK_TYPES = ("", "●", "○")
ARROW_TYPES = ("", "←", "→")

SQR_BTN_W, SQR_BTN_H = 3, 1

DIRECTIONS = [
    namedtuple("Direction", ["y", "x"])(y, x)
    for x in range(-1, 2)
    for y in range(-1, 2)
    if y or x
]