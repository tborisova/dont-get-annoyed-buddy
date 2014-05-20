# http://en.wikipedia.org/wiki/File:Menschenaergern.svg
import random

class InvalidMoveError(Exception):
    pass

class Game:
    IN_PROGRESS = 4
    BLUE_WINS = 0
    GREEN_WINS = 1
    YELLOW_WINS = 2
    RED_WINS = 3
    OUTCOMES = [BLUE_WINS, GREEN_WINS, YELLOW_WINS, RED_WINS, IN_PROGRESS]
    BLUE = 0
    GREEN = 1
    YELLOW = 2
    RED = 3
    START_FOR_COLOR = [0, 10, 20, 30]
    END_FOR_COLOR = [39, 9, 19, 29]
    NEXT_AVAILABLE_POSITION = [0, 10, 20, 30]
    START_FINAL_WALK = [40, 44, 48, 52]
    PATHS_TO_END = {'B1': [40,41,42,43],
                                 'G1': [44,45,46,47],
                                 'Y1': [48,49,50,51],
                                 'R1': [52,53,54,55]}

    COLOR = ['B1', 'G1', 'Y1', 'R1']

    def __init__(self, players ,board=None):
        self._board = board or [0]*56
        self._players = players
        self._player = players[0]

    def outcome(self):
        for player in self._players:
            if player._pawns.count(81) == 4:
                return self.OUTCOMES[player.color()]
        else:
            return self.IN_PROGRESS
    
    @property
    def current_player(self):
        return self._player.color()

    @property
    def previous_player(self):
        if self.current_player == 0:
            return 3
        else:
            return self.current_player - 1
    
    def play(self, pawn, position):
        old_position = self._player.pawn_position(pawn)
        new_position = old_position + position
        self._board[old_position] = 0

        if (new_position in self.forbiden_cells()) and self._player.position_is_in_other_house(new_position):
            new_position = self.next_availabe(old_position, new_position, position)

        if self._board[new_position]:
            for player in self._players:
                if player.color() != self.current_player and position in player._pawns:
                    self._players[self.previous_player].remove_from_position(new_position)
                    break

        if self._player.can_move_to_position(pawn, new_position):
            self._board[new_position] = self._player.color_name()
            self._player.move_pawn_at(pawn, new_position)

        self.change_current_player()

    def next_availabe(self, old_position, new_position, moves):
        if new_position in Game.PATHS_TO_END['B1']:
            return Game.START_FOR_COLOR[0] + (moves - ((Game.END_FOR_COLOR[0] - old_position) + new_position - Game.END_FOR_COLOR[0] - 1))
        if new_position in Game.PATHS_TO_END['G1']:
            return Game.START_FOR_COLOR[1] + (Game.END_FOR_COLOR[1] - old_position + new_position - Game.END_FOR_COLOR[1] - 1) 
        if new_position in Game.PATHS_TO_END['Y1']:
            return Game.START_FOR_COLOR[2] + (Game.END_FOR_COLOR[2] - old_position + new_position - Game.END_FOR_COLOR[2] - 1) 
        if new_position in Game.PATHS_TO_END['R1']:
            return Game.START_FOR_COLOR[3] + (Game.END_FOR_COLOR[3] - old_position + new_position - Game.END_FOR_COLOR[3] - 1)

    def forbiden_cells(self):
        return Game.PATHS_TO_END['B1'] + Game.PATHS_TO_END['Y1'] + Game.PATHS_TO_END['G1'] + Game.PATHS_TO_END['R1']    

    def valid_move(self, pawn, position):
        pawn >= 1 and pawn <= 4 and position >= 0 and position <= 56

    def change_current_player(self):
        if self.current_player == Game.RED:
            self._player = self._players[0]
        else:
            self._player = self._players[self.current_player + 1]
        
    def at(self, position):
       return self._board[position]

class Player:
    
    def __init__(self, color):
        self._color = color
        self._pawns = [Game.START_FOR_COLOR[color]]*4

    def color(self):
        return self._color

    def pawn_position(self, pawn_index):
        return self._pawns[pawn_index - 1]

    def move_pawn_at(self, pawn, position):
        if self.is_at_end(pawn):
            self._pawns[pawn - 1] = START_FINAL_WALK[self._color]
        else:
            self._pawns[pawn - 1] = position

    def remove_from_position(self, position):
        for index, pawn in enumerate(self._pawns):
            if pawn == position:
                self._pawns[index] = Game.START_FOR_COLOR[self.color()]

    def throw_dice(self):
        return random.randint(1,6)

    def can_throw_again(self, dice):
        return dice == 6

    def color_name(self):
        return Game.COLOR[self._color]

    def is_at_end(self, pawn):
        return self._pawns[pawn - 1] == Game.END_FOR_COLOR[self._color]

    def  position_is_in_other_house(self, position):
        b = {key for key in Game.PATHS_TO_END if key != self.color_name()}
        for key in b:
            if position in Game.PATHS_TO_END[key]:
                return True
        return False

    def can_move_to_position(self, pawn, position):
        if self._pawns[pawn - 1] in Game.PATHS_TO_END[self.color_name()]:
            return position <= Game.PATHS_TO_END[self.color_name()][3]
        return True