import random


class Player:

    def __init__(self):
        self._pawns = [-1]*4

    def move_pawn(self, pawn, moves):
        if self._pawns[pawn - 1] != -1:
            old_position = self.path.index(self._pawns[pawn - 1])
        else:
            old_position = -1
        self._pawns[pawn - 1] = self.path[moves + old_position]
        return self._pawns[pawn - 1]

    def pawn_is_in_house(self, pawn):
        return self._pawns[pawn - 1] == self.path[-1]

    def pawn_is_not_in_field(self, pawn):
        return self._pawns[pawn - 1] == -1

    def throw_dice(self):
        self._dice = random.randint(1, 6)
        return self._dice

    def can_throw_again(self):
        return self._dice == 6

    def all_pawns_are_in_house(self):
        return all(self.pawn_is_in_house(pawn) for pawn in range(0, 3))

    def available_pawns(self, dice):
        available = [index + 1 for index in range(0, 3)
            if self.pawn_can_move(index + 1)]

        if dice == 6:
            pawn = next(index + 1 for index in range(0, 3)
                if self.pawn_is_not_in_field(index + 1))
            available.append(pawn)

        return available

    def pawn_can_move(self, pawn):
        return not self.pawn_is_in_house(pawn) and \
        not self.pawn_is_not_in_field(pawn)

    def get_pawn_position(self, pawn):
        return self._pawns[pawn - 1]

    def remove_pawn_from_position(self, position):
        pawn_index = self._pawns.index(position)
        self._pawns[pawn_index] = -1


class RedPlayer(Player):
    PATH = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, 3, 4, \
    5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, \
    23, 24, 25, 26, 27, 28, 29, 52, 53, 54, 55, 56]
    COLOR = 'R'

    @property
    def color(self):
        return RedPlayer.COLOR

    @property
    def path(self):
        return RedPlayer.PATH


class BluePlayer(Player):
    PATH = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, \
    17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
    35, 36, 37, 38, 39, 40, 41, 42, 43, 56]
    COLOR = 'B'

    @property
    def color(self):
        return BluePlayer.COLOR

    @property
    def path(self):
        return BluePlayer.PATH


class YellowPlayer(Player):
    PATH = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
    35, 36, 37, 38, 39, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, \
    13, 14, 15, 16, 17, 18, 19, 48, 49, 50, 51, 56]
    COLOR = 'Y'

    @property
    def color(self):
        return YellowPlayer.COLOR

    @property
    def path(self):
        return YellowPlayer.PATH


class GreenPlayer(Player):
    PATH = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, \
    3, 4, 5, 6, 7, 8, 9, 44, 45, 46, 47, 56]
    COLOR = 'G'

    @property
    def color(self):
        return GreenPlayer.COLOR

    @property
    def path(self):
        return GreenPlayer.PATH