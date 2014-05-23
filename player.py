import random

class Player:

    def __init__(self):
        self._pawns = [-1]*4

    def move_pawn(self, pawn, moves):
        if self._pawns[pawn - 1] != -1:
            self._pawns[pawn - 1] = self.path[moves + self.path.index(self._pawns[pawn - 1])]
        else:
            self._pawns[pawn - 1] = self.path[moves - 1]

    def pawn_is_in_house(self, pawn):
        return self._pawns[pawn - 1] == self.path[-1]

    def pawn_is_not_in_field(self, pawn):
        return self._pawns[pawn - 1] == -1

    def throw_dice(self):
        return random.randint(1,6)

    def can_throw_again(self, dice):
        return dice == 6

class RedPlayer(Player):
    PATH = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, 3, 4, \
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, \
    23, 24, 25, 26, 27, 28, 29, 52, 53, 54, 55, 56]

    @property
    def color(self):
        return 'R'

    @property
    def path(self):
        return RedPlayer.PATH
    

class BluePlayer(Player):
    PATH = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, \
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
    35, 36, 37, 38, 39, 40, 41, 42, 43, 56]

    @property
    def color(self):
        return 'B'

    @property
    def path(self):
        return BluePlayer.PATH
    
class YellowPlayer(Player):
    PATH = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
    35, 36, 37, 38, 39, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, \
    13, 14, 15, 16, 17, 18, 19, 48, 49, 50, 51, 56]

    @property
    def color(self):
        return 'Y'

    @property
    def path(self):
        return YellowPlayer.PATH
    
class GreenPlayer(Player):
    PATH = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, \
    3, 4, 5, 6, 7, 8, 9, 44, 45, 46, 47, 56]

    @property
    def color(self):
        return 'G'

    @property
    def path(self):
        return GreenPlayer.PATH
    