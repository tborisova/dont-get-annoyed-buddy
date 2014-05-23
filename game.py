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
    
    def play(self, pawn, moves):
        if self._player.can_make_moves(pawn, moves):
            old_position = self._player.pawn_position(pawn)
            new_position = self._player.move_pawn_at(pawn, moves)
            if new_position == -1:
                self._board[old_position] = 0
            else:
                if self._board[new_position] and self._board[new_position] != self._player.color_name():
                    self.remove_from_position(new_position)
                self.update_board(new_position, old_position)
        self.change_current_player()
    
    def update_board(self, new_position, old_position):
        self._board[new_position] = self._player.color_name()
        self._board[old_position] = 0
    
    def remove_from_position(self, position):
        previous_player = self._board[position]
        player_name = Game.COLOR.index(previous_player)
        self._players[player_name].remove_from_position(position)

    def valid_move(self, pawn, position):
        pawn >= 1 and pawn <= 4 and position >= 0 and position <= 56

    def change_current_player(self):
        if self._player._color == Game.RED:
            self._player = self._players[0]
        else:
            self._player = self._players[self._player._color + 1]
        
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
            return position in Game.PATHS_TO_END[self.color_name()]
        return True

    def will_go_in_house(self, pawn, moves):
        if self._pawns[pawn - 1] == Game.PATHS_TO_END[self.color_name()][3] and moves == 1:
            self._pawns[pawn - 1] = -1
            return True
        return False

    def pawn_is_on_field(self, pawn):
        return self._pawns[pawn - 1] != -1

    def move_pawn_at(self, pawn, moves):
        new_position = self.pawn_position(pawn) + moves

        if self.is_at_end(pawn):
            self._pawns[pawn - 1] = Game.START_FINAL_WALK[self._color]
            if self.can_make_moves(pawn, moves - 1):
                new_position = self.pawn_position(pawn) + moves - 1
        elif new_position >= Game.END_FOR_COLOR[self._color] and self._pawns[pawn - 1] <= Game.END_FOR_COLOR[self._color]:
            moves_to_start_of_final_walk = Game.END_FOR_COLOR[self._color] - self._pawns[pawn - 1]
            moves_to_make = moves - moves_to_start_of_final_walk
            new_position = Game.PATHS_TO_END[self.color_name()][0] + moves_to_make
        elif self.will_go_in_house(pawn, moves):
            new_position = -1
        elif self.position_is_in_other_house(new_position):
            new_position = self.next_availabe(new_position, moves)
        self._pawns[pawn - 1] = new_position  
        
        return new_position

    def can_make_moves(self, pawn, moves):
        if self._pawns[pawn - 1] in Game.PATHS_TO_END[self.color_name()]:
            return self._pawns[pawn - 1] + moves in Game.PATHS_TO_END[self.color_name()]
        else:
            return self.pawn_is_on_field(pawn)

    def next_availabe(self, new_position, moves):
        for color_name in Game.PATHS_TO_END:
            if color_name != self.color_name() and new_position in Game.PATHS_TO_END[color_name]:
                index = Game.COLOR.index(color_name)
                start = Game.START_FOR_COLOR[index]
                end = Game.END_FOR_COLOR[index]
                return start + (moves - ((end - (new_position - moves)) + new_position - end - 1))