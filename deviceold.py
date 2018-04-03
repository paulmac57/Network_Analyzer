#was piece

from configurations import *
import exceptions


def create_device (device, color='white'):  # pretend color is manufacturer and white is cisco
    if isinstance(device, str):
        if device.upper() in SHORT_NAME.keys():
            color = "white"
            device = SHORT_NAME[device.upper()]
        device = device.capitalize()
        if device in SHORT_NAME.values():
            return eval("{classname}(color)".format(classname=device))
    raise exceptions.NetConfError("invalid device name: '{}'".format(device))

def get_numeric_notation(rowcol):
    row, col = rowcol
    return int(col)-1, X_AXIS_LABELS.index(row)

class Device():

    def __init__(self, color):
        self.name = self.__class__.__name__.lower()
        

        if color == 'black':
            self.name = self.name.lower()
        elif color == 'white':
            self.name = self.name.upper()
        self.color = color
   
    def keep_reference(self, model):
        self.model = model

class Router(Device):
    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
    max_distance = 20
    def moves_available(self,current_position):
        return super(Router, self).moves_available (current_position, self.directions, self.max_distance)

class Switch(Device):
    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
    max_distance = 20
    def moves_available(self,current_position):
        return super(Switch, self).moves_available (current_position, self.directions, self.max_distance)



##class King(Device):
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(King, self).moves_available (current_position, self.directions, self.max_distance)
##
##class Queen(Device):
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(Queen, self).moves_available (current_position, self.directions, self.max_distance)
##
##class Rook(Device):
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(Rook, self).moves_available(current_position, self.directions, self.max_distance)
##
##class Bishop(Device):
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(Bishop, self).moves_available (current_position, self.directions, self.max_distance)
##
##class Knight(Device):
##
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(Bishop, self).moves_available (current_position, self.directions, self.max_distance)
##
##class Pawn(Device):
##
##    directions = ORTHOGONAL_POSITIONS + DIAGONAL_POSITIONS
##    max_distance = 20
##    def moves_available(self,current_position):
##        return super(Pawn, self).moves_available (current_position, self.directions, self.max_distance)
##


##def moves_available(self, current_position, directions, distance):
##        model = self.model
##        allowed_moves = []
##        device = self
##        start_row, start_column = get_numeric_notation(current_position)
##        for x, y in directions:
##            collision = False
##            for step in range(1, distance + 1):
##                if collision:
##                    break
##                destination = start_row + step * x, start_column + step * y
##                if self.possible_position(destination) not in model.all_occupied_positions():
##                    allowed_moves.append(destination)
##                elif self.possible_position(destination) in model.all_positions_occupied_by_color (piece.color):
##                    collision = True
##                else:
##                    allowed_moves.append(destination)
##                    collision = True
##        allowed_moves = filter(model.is_on_board, allowed_moves)
##        return map(model.get_alphanumeric_position, allowed_moves)
##
##def possible_position(self, destination): #4.04 piece.py
##    return self.model.get_alphanumeric_position(destination)
##
##def all_positions_occupied_by_color(self, color): #4.04 model.py
##    result = []
##    for position in self.keys():
##        piece = self.get_piece_at(position)
##        if piece.color == color:
##            result.append(position)
##    return result
##
##def all_occupied_positions(self): #4.04 model.py
##    return self.all_positions_occupied_by_color('white') + self.all_positions_occupied_by_color('black')    
##    
##
