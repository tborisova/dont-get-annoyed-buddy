import re
import os
from game import Game
from game import Player
# 42 - 39 = 3
# 4 - 3 са стъпките до началото на края
# след това + 1 стъпка за да стигнеш до началото
# значи ти остават хвърлените стъпки - 2 
# хвърлила съм 4
# правя m стъпки до старт на цвета и след това к стъпки,които ми остават
BOARD = """
                  38 39 00
                  37 40 01
            r     36 41 02      b
                  35 42 03
      30 31 32 33 34 43 04 05 06 07 08
      29 44 45 46 47    51 50 49 48 09
      28 27 26 25 24 55 14 13 12 11 10
                  23 54 15
                  22 53 16
           y      21 52 17    g
                  20 19 18
"""
class CLI:
    def __init__(self):
        self._players = [Player(Game.BLUE), Player(Game.GREEN), Player(Game.YELLOW), Player(Game.RED)]
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
        elif outcome == Game.GREEN_WINS:
            print("green wins")
        elif outcome == Game.YELLOW_WINS:
            print("yellow wins")
        else:
            print("It's a tie (⧓)!")


    def _clear(self):
        os.system('clear')

    def _draw_board(self):
        b = BOARD[:]
        for index, cell in enumerate(self._game._board):
            original_index = index
            if index in range(0, 10):
                index = '0' + str(index)
            else:
                index = str(index)
            if cell:
                b = b.replace(index, self._game.at(original_index), 1)
            else:
                b = b.replace(index, '**',  1)
        print(b)
        print(self._game._board)

    def _get_move(self):
        print("Player: {0} is about to throw dice".format(self._game._player.color_name()))
        dice = self._game._player.throw_dice()
        print("You throw: {0}".format(dice))
        print("Choose pawn to move:[1,2,3,4]:", end='')
        pawn = int(input())
        position = dice
        
        return [pawn, position]


CLI().play()
# print(BOARD)