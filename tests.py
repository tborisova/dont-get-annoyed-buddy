import unittest

from game import Game, InvalidMoveError, Player

class PlayerTest(unittest.TestCase):
    def testAllPawnsAreInHome(self):
        player = Player(Game.BLUE)

        self.assertEqual(player.pawn_position(1), 0)
        self.assertEqual(player.pawn_position(2), 0)
        self.assertEqual(player.pawn_position(3), 0)
        self.assertEqual(player.pawn_position(4), 0)

    def testMovePawnChangesPawnPosition(self):
        player = Player(Game.BLUE)

        player.move_pawn_at(1, 3, 3)
        self.assertEqual(player.pawn_position(1), 3)
        self.assertEqual(player.pawn_position(2), 0)
        self.assertEqual(player.pawn_position(3), 0)
        self.assertEqual(player.pawn_position(4), 0)



class GameTest(unittest.TestCase):
    def create_game(self, board=[0]*56):
        players = [Player(Game.BLUE), Player(Game.GREEN), Player(Game.YELLOW), Player(Game.RED)]
        return Game(players, board[:])
    
    def testDeterminingInProgress(self):
        game = self.create_game()
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)

        game = self.create_game([0]*20 + [1]*36)
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)

        game = self.create_game()
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)
    
    def testPlayChangesCurrentPlayer(self):
        game = self.create_game()
        self.assertEqual(game.current_player, Game.BLUE)     
        
        game.play(1,2)
        self.assertEqual(game.current_player, Game.GREEN)
        
        game.play(1,4)
        self.assertEqual(game.current_player, Game.YELLOW)

        game.play(1,3)
        self.assertEqual(game.current_player, Game.RED)
        
        game.play(1,0)            
        self.assertEqual(game.current_player, Game.BLUE)
       
    def testPlayChangesBoard(self):
        game = self.create_game()
        
        game.play(0, 4) 
        self.assertEqual(game._board[4], 'B1')
        self.assertTrue('B1' in game._board)

        game.play(1, 8)
        self.assertEqual(game._board[18], 'G1')
        self.assertTrue('G1' in game._board)

    def testPlayChangesPawnsPosition(self):
        game = self.create_game()

        game.play(1, 4)
        self.assertEqual(game._players[0].pawn_position(1), 4)
        
        game.play(1, 8)
        self.assertEqual(game._players[1].pawn_position(1), 18)
        
        game.play(2, 3)
        self.assertEqual(game._players[2].pawn_position(2), 23)
    
    def xtestPlayerMovesPawnOverOtherPlayersPawn(self):
        game = self.create_game()

        game.play(1, 4)
        game.play(1, 4)
        self.assertEqual(game._players[0].pawn_position(1),  0)
    
    def testPlayerMovesPawnOverHisOtherPawn(self):
        game = self.create_game()

        game.play(1, 7)
        game.play(1, 4)
        game.play(1, 2)
        game.play(1, 1)
        game.play(2, 7)
        self.assertEqual(game._players[0].pawn_position(1), 7)
        self.assertEqual(game._players[0].pawn_position(2), 7)
    
    def xtestInvalidMoveIfOutsideBoard(self):
        game = self.create_game()

        self.assertRaises(InvalidMoveError, game.play(1, 82))

    def testGameEndsWhenPlayerHasAllPawnsInTheFinale(self):
        game = self.create_game()

        game._players[0]._pawns = [81, 81, 81, 81]
        self.assertEqual(game.outcome(), Game.BLUE_WINS)
        
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game._players[1]._pawns = [81, 81, 81, 81]
        self.assertEqual(game.outcome(), Game.RED_WINS)

    def testOldPositionToPawnIsUnset(self):
        game = self.create_game()
        game.play(1, 2)
        game.play(1, 4)
        game.play(1, 2)
        game.play(1, 1)
        game.play(1, 9)
        self.assertEqual(game._board[2], 0)
    
    def testPlayerStartPosition(self):
        game = self.create_game()

        game.play(1, 1)

        self.assertEqual(game._board[1], 'B1')
    
        game.play(1, 2)

        self.assertEqual(game._board[12], 'G1')

    def testsPlayerCantGoInOtherHouse(self):
        game = self.create_game()

        game._player = game._players[3]
        game._player._pawns[0] = 34

        self.assertEqual(game._board[0], 0)

        game.play(1, 6)

        self.assertEqual(game._board[1], 'R1')

    def testThatWhenPlayerIsnHouseItCanOnlyMoveInsideNotInTheField(self):
        game = self.create_game()

        game._player._pawns[0] = 40
        game.play(1, 6)
        self.assertEqual(game._board[46], 0)

        game = self.create_game()

        game._player._pawns[0] = 41
        game.play(1, 3)
        self.assertEqual(game._board[44], 0)

        game = self.create_game()

        game._player._pawns[0] = 42
        game.play(1, 2)
        self.assertEqual(game._board[44], 0)
        
        game = self.create_game()
        game._player._pawns[0] = 42
        
        game.play(1, 1)
        self.assertEqual(game._board[43], 'B1')
    
    def GameIsOverWhenAllPawnsAreInHouse(self):
        game = self.create_game()
        game._player._pawns[0] = 42
        game._player._pawns[1] = 43
        game._player._pawns[2] = 43
        game._player._pawns[3] = 43
        
        game.play(1, 1)
        self.assertEqual(game._board[43], 'B1')
        
        self.assertEqual(game.outcome(), Game.BLUE_WINS)
if __name__ == '__main__':
    unittest.main()

