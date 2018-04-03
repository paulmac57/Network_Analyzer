from configurations import *
import device  # import piece
import exceptions

class Model(dict):

    
    counter = 1   # fullmove_number
    history = []

    def __init__(self):
        self.reset_to_initial_locations()

    def delete_device_at(self,position):
        self.pop(position)
        
    def get_device_at(self, position):
        print("Device is (%s) at position (%s)" % (self,position))
        return self.get(position)

    def get_alphanumeric_position(self, rowcol):
        if self.is_on_board(rowcol):
            row, col = rowcol
            return "{}{}".format(X_AXIS_LABELS[col], Y_AXIS_LABELS[row])

    def is_on_board(self, rowcol):
        row, col = rowcol
        return 0 <= row <= 20 and 0 <= col <= 20

    def reset_network_data(self):
        history = []

    def reset_to_initial_locations(self):
         self.clear()
         for position, value in START_PIECES_POSITION.items():
           self[position] = device.create_device(value)
           self[position].keep_reference(self)
##         self.player_turn = 'white'

   

##    def get_all_available_moves(self, color):
##        result = []
##        for position in self.keys():
##            device = self.get_device_at(position)
##            moves = device.moves_available(position)
##            if moves:
##                result.extend(moves)
##        return result

    def pre_move_validation(self, initial_pos, final_pos):
        initial_pos, final_pos = initial_pos.upper(), final_pos.upper()
        device = self.get_device_at(initial_pos)
        device_at_destination = self.get_device_at(final_pos)
        self.move(initial_pos, final_pos)
        self.update_statistics(
               device, device_at_destination, initial_pos, final_pos)

        #self.change_player_turn(device.color)

##        try:
##            device_at_destination = self.get_piece_at(final_pos)
##        except:
##            device_at_destination = None
##        if self.player_turn != device.color:
##            raise exceptions.NotYourTurn("Not " + piece.color + "'s turn!")
##        enemy = ('white' if piece.color == 'black' else 'black')
##        moves_available = device.moves_available(initial_pos)
##        if final_pos not in moves_available:
##            raise exceptions.InvalidMove
##        if self.get_all_available_moves(enemy):
##            if self.will_move_cause_check(initial_pos, final_pos):
##                raise exceptions.Check
##        if not moves_available and self.is_king_under_check(piece.color):
##            raise exceptions.CheckMate
##        elif not moves_available:
##            raise exceptions.Draw
##        else:
##            self.move(initial_pos, final_pos)

##            self.change_player_turn(piece.color)


        

    def move(self, start_pos, final_pos):
        self[final_pos] = self.pop(start_pos, None)

    def update_statistics(self, device, dest, start_pos, end_pos):
        
        abbr = device.name
##        if abbr == 'pawn':
##            abbr = ''
##            self.halfmove_clock = 0
        if dest is None:
            move_text = abbr + end_pos.lower()
        else:
            move_text = abbr + 'x' + end_pos.lower()
           
        self.history.append(move_text)

##    def change_player_turn(self, color):
##        
##        self.player_turn = 'white'  
