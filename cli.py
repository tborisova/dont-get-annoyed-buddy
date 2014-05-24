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
            self._clear()
            self._draw_board()
            position_and_pawn = self._get_move()
            while len(position_and_pawn) == 0:  
                self._game.change_player()
                position_and_pawn = self._get_move()
            position = position_and_pawn[1]
            self._game.play(position_and_pawn[0], position_and_pawn[1])
            

        self._clear()
        self._draw_board()

        outcome = self._game.outcome()

        if outcome == BluePlayer.COLOR:
            print("Blue wins!")
        elif outcome == RedPlayer.COLOR:
            print("Red wins!")
        elif outcome == GreenPlayer.COLOR:
            print("Green wins")
        elif outcome == YellowPlayer.COLOR:
            print("Yellow wins")

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

    def _get_move(self):
        print("Player: {0} is about to throw dice".format(self._game.current_player.color))
        print("Enter 'y' to throw dice")
        choice = str(input())
        if choice == 'y':
            dice = self._game.current_player.throw_dice()
            print("You throw: {0}".format(dice))
            if len(self._game.current_player.available_pawns(dice)) > 0:
                pawn = None
                while pawn is None:
                    print("Choose pawn to move:{0}:".format(self._game.current_player.available_pawns(dice)), end='')
                    pawn = int(input())
                    position = dice
                    if pawn not in self._game.current_player.available_pawns(dice):
                        pawn = None
                return [pawn, position]
            else:
                print("You can't move any pawn")
                return []

CLI([RedPlayer(), BluePlayer(), GreenPlayer(), YellowPlayer()]).play()