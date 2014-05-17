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

        player.move_pawn_at(1, 3)
        self.assertEqual(player.pawn_position(1), 3)
        self.assertEqual(player.pawn_position(2), 0)
        self.assertEqual(player.pawn_position(3), 0)
        self.assertEqual(player.pawn_position(4), 0)



class GameTest(unittest.TestCase):
    def testDeterminingInProgress(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        
        game = Game(players, [0]*81)
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)

        game = Game(players, [0]*20 + [1]*61)
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)

        game = Game(players)
        self.assertEqual(game.outcome(), Game.IN_PROGRESS)
    
    def testPlayChangesCurrentPlayer(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        self.assertEqual(game.current_player, Game.BLUE)     
        
        game.play(1,20)
        self.assertEqual(game.current_player, Game.RED)
        
        game.play(1,40)
        self.assertEqual(game.current_player, Game.YELLOW)

        game.play(1,60)
        self.assertEqual(game.current_player, Game.GREEN)
        
        game.play(1,0)            
        self.assertEqual(game.current_player, Game.BLUE)
       
    def testPlayChangesBoard(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game.play(0, 47) 
        self.assertEqual(game._board[47], 1)
        self.assertEqual(sum(game._board), 1)

        game.play(1, 48)
        self.assertEqual(game._board[48], 1)
        self.assertEqual(sum(game._board), 2)

    def testPlayChangesPawnsPosition(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game.play(1, 47)
        self.assertEqual(game._players[0].pawn_position(1), 47)
        
        game.play(1, 48)
        self.assertEqual(game._players[1].pawn_position(1), 48)
        
        game.play(2, 3)
        self.assertEqual(game._players[2].pawn_position(2), 3)
    
    def testPlayerMovesPawnOverOtherPlayersPawn(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game.play(1, 47)
        game.play(1, 47)
        self.assertEqual(game._players[0].pawn_position(1),  0)
    
    def testPlayerMovesPawnOverHisOtherPawn(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game.play(1, 47)
        game.play(1, 4)
        game.play(1, 2)
        game.play(1, 1)
        game.play(2, 47)
        self.assertEqual(game._players[0].pawn_position(1), 47)
        self.assertEqual(game._players[0].pawn_position(2), 47)
    
    def xtestInvalidMoveIfOutsideBoard(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        with self.assertRaises(InvalidMoveError):
            game.play(1, 82)

    def testGameEndsWhenPlayerHasAllPawnsInTheFinale(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game._players[0]._pawns = [81, 81, 81, 81]
        self.assertEqual(game.outcome(), Game.BLUE_WINS)
        
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game._players[1]._pawns = [81, 81, 81, 81]
        self.assertEqual(game.outcome(), Game.RED_WINS)

    def testOldPositionToPawnIsUnset(self):
        players = [Player(Game.BLUE), Player(Game.RED), Player(Game.YELLOW), Player(Game.GREEN)]
        game = Game(players, [0]*81)
        
        game.play(1, 47)
        game.play(1, 4)
        game.play(1, 2)
        game.play(1, 1)
        game.play(1, 48)
        self.assertEqual(game._board[47], 0)
        
if __name__ == '__main__':
    unittest.main()

