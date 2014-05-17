# http://en.wikipedia.org/wiki/File:Menschenaergern.svg
import random

class InvalidMoveError(Exception):
    pass

class Game:
    IN_PROGRESS = 4
    BLUE_WINS = 0
    RED_WINS = 1
    GREEN_WINS = 2
    YELLOW_WINS = 3
    OUTCOMES = [BLUE_WINS, RED_WINS, GREEN_WINS, YELLOW_WINS, IN_PROGRESS]
    BLUE = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    START_FOR_COLOR = [0, 10, 20, 30]
    END_FOR_COLOR = [39, 9, 19, 29]
    START_FINAL_WALK = [40, 44, 48, 52]
    PATH_TO_BLUE = [40,41,42,43]
    PATH_TO_RED = [44,45,46,47]
    PATH_TO_GREEN = [48,49,50,51]
    PATH_TO_YELLOW = [52,53,54,55]
    
    COLOR = ['B1', 'R1', 'G1', 'Y1']

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

    def play(self, pawn, position):
        old_position = self._player.pawn_position(pawn)
        self._board[old_position] = 0
        if self._board[position]:
            for player in self._players:
                if player.color() != self.current_player and position in player._pawns:
                    player.remove_from_position(position)
                    break
        else:
            self._board[position] = self._player.color_name()
        
        self._player.move_pawn_at(pawn, position)
        self.change_current_player()

    def valid_move(self, pawn, position):
        pawn >= 1 and pawn <= 4 and position >= 0 and position <=81

    def change_current_player(self):
        if self.current_player == Game.YELLOW:
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