from configparser import ConfigParser

NUMBER_OF_ROWS = 10
NUMBER_OF_COLUMNS = 10
DIMENSION_OF_EACH_SQUARE = 128  # denoting 64 pixels
X_AXIS_LABELS = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R')
Y_AXIS_LABELS = (1, 2, 3, 4, 5, 6, 7, 8,9,10,11,12,13,14,15,16,17,18,19,20)

START_PIECES_POSITION = {"B3": "R", "E5": "S"}
"""
START_PIECES_POSITION = {
    "A8": "r", "B8": "n", "C8": "b", "D8": "q", "E8": "k", "F8": "b", "G8": "n", "H8": "r",
    "A7": "p", "B7": "p", "C7": "p", "D7": "p", "E7": "p", "F7": "p", "G7": "p", "H7": "p",
    "A2": "P", "B2": "P", "C2": "P", "D2": "P", "E2": "P", "F2": "P", "G2": "P", "H2": "P",
    "A1": "R", "B1": "N", "C1": "B", "D1": "Q", "E1": "K", "F1": "B", "G1": "N", "H1": "R"
}
"""
HIGHLIGHT_COLOR = "#2EF70D"

#SHORT_NAME = {'R': 'Rook',  'N': 'Bishop',  'B': 'Bishop',  'Q': 'Queen', 'K': 'King',  'P': 'Pawn'}

SHORT_NAME = {'R': 'Router', 'S': 'Switch'}

ORTHOGONAL_POSITIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
DIAGONAL_POSITIONS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
KNIGHT_POSITIONS = ((-2, -1), (-2, 1), (-1, -2), (-1, 2),
                    (1, -2), (1, 2), (2, -1), (2, 1))


'''
User Modifiable Options
'''
config = ConfigParser()
config.read('serial.ini')
PORT = config.get('serial_comms', 'port', fallback="com3")
SPEED = config.get('serial_comms', 'speed', fallback="9600")
BITS = config.get('serial_comms', 'bits', fallback="8")
PARITY = config.get('serial_comms', 'parity', fallback="none")
STOP = config.get('serial_comms', 'stop', fallback="1")
HIGHLIGHT_COLOR = config.get(
    'chess_colors', 'highlight_color', fallback="#2EF70D")
BOARD_COLOR_1 = "azure"
BOARD_COLOR_2 = "alice blue"
    
