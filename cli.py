import re
import os
from game import Game
from game import Player

BOARD = """
             0 * *
             1 * *
             2 * *
    r r      3 * *    b b 
    r r      4 * *    b b
             5 * *
             6 * *
20 * * * * * *     * * * * * * 40
* * * * * * *     * * * * * * *
* * * * * * *     * * * * * * *
             * * *
             * * *
   y y       * * *    g g
   y y       * * *    g g
             * * *
             * * *
             30 * *
"""
class CLI:
    def __init__(self):
        self._players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        self._game = Game(self._players)

    def play(self):
        while self._game.outcome() == Game.IN_PROGRESS:
            self._clear()
            self._draw_board()

            position = None
            while position is None:
                position_and_pawn = self._get_move()
                position = position_and_pawn[1]
            self._game.play(position_and_pawn[0], position_and_pawn[1])

            self._clear()
            self._draw_board()

        outcome = self._game.outcome()

        if outcome == Game.BLUE_WINS:
            print("Whoo! BLUE wins!")
        elif outcome == Game.RED_WINS:
            print("Ooooh wins!")
        else:
            print("It's a tie (⧓)!")

    def _clear(self):
        os.system('clear')

    def _draw_board(self):
        b = BOARD[:]
        for index, cell in enumerate(self._game._board):
            if cell:
                b = b.replace(str(index), cell, 1)
            else:
                b = b.replace(str(index), '*', 1)
        print(b)

    def _get_move(self):
        dice = self._game._player.throw_dice()
        print("You throw: {0}".format(dice))
        print("Choose pawn to move:[1,2,3,4]:", end='')
        pawn = int(input())
        position = dice
        
        return [pawn, position]


CLI().play()
