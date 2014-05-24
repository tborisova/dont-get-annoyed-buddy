import unittest

from player import Player,  RedPlayer, BluePlayer, GreenPlayer, YellowPlayer
from game import Game

class GameTest(unittest.TestCase):

    def create_game(self):
        return Game([RedPlayer(), BluePlayer(), GreenPlayer(), YellowPlayer()])
    
    def testOutcomeInProgress(self):
        game = self.create_game()

        self.assertEqual(game.outcome(), Game.IN_PROGRESS)

    def testRedWins(self):
        game = self.create_game()

        game._players[0]._pawns = [56]*4
        self.assertEqual(game.outcome(), 'R')


    def testBlueWins(self):
        game = self.create_game()

        game._players[1]._pawns = [56]*4
        self.assertEqual(game.outcome(), 'B')

    def testGreenWins(self):
        game = self.create_game()

        game._players[2]._pawns = [56]*4
        self.assertEqual(game.outcome(), 'G')

    def testYellowWins(self):
        game = self.create_game()

        game._players[3]._pawns = [56]*4
        self.assertEqual(game.outcome(), 'Y')

    def testBoardIsEmptyOnStart(self):
        game = self.create_game()

        self.assertEqual(sum(game._board), 0)

    def testWhenPlayerMovesPawnBoardHasNewPosition(self):
        game = self.create_game()

        game.play(1, 2)
        
        index = game._players[0]._pawns[0]
        
        self.assertEqual(game._board[index], 'R1')

    def testWhenPlayerMovesPawnHItsOldPositionIsUnset(self):
        game = self.create_game()

        game.play(1, 2)
        index = game._players[0]._pawns[0]
        game._player_index = 0
        game.play(1, 4)
        new_index = game._players[0]._pawns[0]
        
        self.assertEqual(game._board[new_index], 'R1')
        self.assertEqual(game._board[index], 0)

    def testWhenPlayerMakeMoveNextPlayerStartsToPlay(self):
        game = self.create_game()

        game.play(1, 2)
        self.assertEqual(game.current_player, game._players[1])
        
        game.play(1, 2)
        self.assertEqual(game.current_player, game._players[2])
        
        game.play(1, 2)
        self.assertEqual(game.current_player, game._players[3])
    
    def testWhenPlayerPawnStepsOverBrotherPawnTheyBothStay(self):
        game = self.create_game()

        game.play(1, 2)
        game._player_index = 0
        game.play(2, 2)
        game._player_index = 0
        index = game.current_player._pawns[0]

        self.assertEqual(game.current_player._pawns[0], game.current_player._pawns[1])
        self.assertEqual(game._board[index], 'R2')

    def testWhenPlayerPawnStepsOverOtherPlayerPawnTheLastIsRemovedFromField(self):
        game = self.create_game()

        game._board[31] = 'B1'
        game._players[1]._pawns[0] = 31
        
        game._player_index = 0
        game.play(1, 2)

        self.assertEqual(game._board[31], 'R1')
        self.assertEqual(game._players[1]._pawns[0], -1)

    def testThatGameKnowsWhatPawnsAreOnBoard(self):
        game = self.create_game()

        game.play(1, 2)
        game.play(2, 2)
        game.play(3, 2)
        game.play(4, 2)

        self.assertEqual(game.at(31), 'R1')
        self.assertEqual(game.at(1), 'B2')
        self.assertEqual(game.at(11), 'G3')
        self.assertEqual(game.at(21), 'Y4')
        self.assertEqual(game._board, [0, 'B2', 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                       'G3', 0, 0, 0, 0, 0, 0, 0, 0, 0, 'Y4', 
                                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 'R1', 0, 0, 
                                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

if __name__ == '__main__':
    unittest.main()

