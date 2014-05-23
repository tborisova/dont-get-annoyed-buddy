import unittest

from player import Player,  RedPlayer

class PlayerTest(unittest.TestCase):

    def testIsPlayerMove(self):
        player = RedPlayer()

        player.move_pawn(1, 2)
        self.assertEqual(player._pawns[0], 31)
        
        player.move_pawn(1, 6)
        self.assertEqual(player._pawns[0], 37)
       
        player.move_pawn(1, 4)
        self.assertEqual(player._pawns[0], 1)
         
    def testPawnIsNotOnField(self):
        player = RedPlayer()
        self.assertTrue(player.pawn_is_not_in_field(1))

    def testPawnIsInHouse(self):
        player = RedPlayer()
        player._pawns[0] = 56
        self.assertTrue(player.pawn_is_in_house(1))


if __name__ == '__main__':
    unittest.main()

