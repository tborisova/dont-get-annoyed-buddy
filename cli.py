import re
import os
from game import Game
from player import Player, RedPlayer, BluePlayer, GreenPlayer, YellowPlayer

BOARD = """
                  38 39 00
                  37 40 01
            r     36 41 02      b
                  35 42 03
      30 31 32 33 34 43 04 05 06 07 08
      29 52 53 54 55 56 47 46 45 44 09
      28 27 26 25 24 51 14 13 12 11 10
                  23 50 15
                  22 49 16
           y      21 48 17    g
                  20 19 18
"""

class CLI:
    def __init__(self, players):
        self._game = Game(players)

    def play(self):
        while self._game.outcome() == Game.IN_PROGRESS:
            # self._clear()
            self._draw_board()
            position_and_pawn = self._get_move()
            if len(position_and_pawn) > 0:  
                position = position_and_pawn[1]
                self._game.play(position_and_pawn[0], position_and_pawn[1])
            else:
                self._game.change_player()

        self._clear()
        self._draw_board()

        outcome = self._game.outcome()

        if outcome == BluePlayer.COLOR:
            print("Whoo! BLUE wins!")
        elif outcome == RedPlayer.COLOR:
            print("Ooooh wins!")
        elif outcome == GreenPlayer.COLOR:
            print("green wins")
        elif outcome == YellowPlayer.COLOR:
            print("yellow wins")
        else:
            print("It's a tie (⧓)!")


    def _clear(self):
        os.system('clear')

    def _draw_board(self):
        b = BOARD[:]
        print(self._game._board)
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

    def _get_move(self):
        print("Player: {0} is about to throw dice".format(self._game._player.color))
        dice = self._game._player.throw_dice()
        print("You throw: {0}".format(dice))
        if len(self._game._player.available_pawns()) > 0:
            print("Choose pawn to move:{0}:".format(self._game._player.available_pawns()), end='')
            pawn = int(input())
            position = dice
        
            return [pawn, position]
        else:
            return []

CLI([RedPlayer(), BluePlayer(), GreenPlayer(), YellowPlayer()]).play()