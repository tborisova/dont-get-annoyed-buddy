import unittest

from player import Player,  RedPlayer, BluePlayer, GreenPlayer, YellowPlayer

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

    def xtestThrowDiceIsRandomNumber(self):
        #check how to mock
        pass

    def testAllPawnsAreInHouse(self):
        player = RedPlayer()

        player._pawns[0] = player._pawns[1] = player._pawns[2] = 55
        player._pawns[3] = 56

        self.assertFalse(player.all_pawns_are_in_house())

        player._pawns[0] = player._pawns[1] = player._pawns[2] = 56
        self.assertTrue(player.all_pawns_are_in_house())
    
    def testCanThrowAgain(self):
        player = RedPlayer()

        player._dice = 6
        self.assertTrue(player.can_throw_again())

        player._dice = 3
        self.assertFalse(player.can_throw_again())

    def testPlayerKnowsHisAvaiablePawns(self):
        player = RedPlayer()

        self.assertEqual(player.available_pawns(3), [])

        self.assertEqual(player.available_pawns(6), [1])

        player._pawns[0] = 1
        self.assertEqual(player.available_pawns(6), [1, 2])
        player._pawns[1] = 0

        self.assertEqual(player.available_pawns(6), [1, 2, 3])
        player._pawns[2] = 3

        player._pawns[1] = -1
        self.assertEqual(player.available_pawns(2), [1, 3])
    
    def testPawnIsRemovedFromPosition(self):
        player = RedPlayer()

        player._pawns = [1, 34, 4, 5]

        player.remove_pawn_from_position(4)        

        self.assertEqual(player._pawns[0], 1)
        self.assertEqual(player._pawns[1], 34)
        self.assertEqual(player._pawns[2], -1)
        self.assertEqual(player._pawns[3], 5)

    def testBluePlayerSetup(self):
        player = BluePlayer()

        self.assertEqual(player.color, 'B')
        self.assertEqual(player.path, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, \
        17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
        35, 36, 37, 38, 39, 40, 41, 42, 43, 56])

    def testRedPlayerSetup(self):
        player = RedPlayer()

        self.assertEqual(player.color, 'R')
        self.assertEqual(player.path, [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, 3, 4, \
        5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, \
        23, 24, 25, 26, 27, 28, 29, 52, 53, 54, 55, 56])


    def testYellowPlayer(self):
        player = YellowPlayer()

        self.assertEqual(player.color, 'Y')
        self.assertEqual(player.path, [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, \
        35, 36, 37, 38, 39, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, \
        13, 14, 15, 16, 17, 18, 19, 48, 49, 50, 51, 56])

    def testGreenPlayer(self):
        player = GreenPlayer()

        self.assertEqual(player.color, 'G')
        self.assertEqual(player.path, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, \
        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 0, 1, 2, \
        3, 4, 5, 6, 7, 8, 9, 44, 45, 46, 47, 56])

if __name__ == '__main__':
    unittest.main()

