import random
import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from player import *
from game import *

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

class ClientChannel(Channel):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        self.first_time = True
        self.color_class = ''
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################

    # self._server.SendToAll({"action": "message", "message": data['message'], "who": "{0} {1}".format(self.nickname, str(color_class)), 'board' : BOARD}    
    def Network_message(self, data):
        if self._server.player_can_write(self) and self._server.player_now_should_be_prompt_to_pick_a_pawn:
            self._server.player_now_should_be_prompt_to_pick_a_pawn = False
            dice = self._server._game.current_player.throw_dice()
            self._server.current_player_dice = dice
            old_player = type(self._server._game.current_player).__name__
            if len(self._server._game.current_player.available_pawns(dice)) > 0:
                self._server.SendToAll({'action': 'message_throw', 'message': "{0} throw {1}. Now he should choose pawn: {2}".format(old_player, dice, self._server._game.current_player.available_pawns(dice)), 'board': self._server.draw_board()})
            else:
                self._server._game.change_player()
                self._server.SendToAll({'action': 'message_throw', 'message': "{0} throw {1}. But he can't move pawn, so new player: {2}".format(old_player, dice, type(self._server._game.current_player).__name__), 'board': self._server.draw_board()})
                self._server.player_now_should_be_prompt_to_pick_a_pawn = True
        elif self._server.player_can_write(self): #and self._server.player_now_has_picked_a_pawn(self):
            self._server.SendToAll({'action': 'message_throw', 'message': "{0} choose: {1}".format(type(self._server._game.current_player).__name__, data['message']), 'board': self._server.draw_board()})
            self._server.player_now_should_be_prompt_to_pick_a_pawn = True
            self._server._game.change_player()
            self._server._game.play(int(data['message']), self._server.current_player_dice)
            self._server.SendToAll({'action': 'draw_board', 'message': "{0}".format(self._server.draw_board())})


    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()

class ChatServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        self.available_classes = [RedPlayer('R'), BluePlayer('B'), GreenPlayer('G'), YellowPlayer('Y')]
        self.player_to_class = {}
        self.game_started = False
        self.current_player_dice = 0
        self.player_now_should_be_prompt_to_pick_a_pawn = True
        print('Server launched')
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        if len(self.players) < 4:
            print("New Player {0}".format(str(player.addr)))
            self.players[player] = True
            self.SendPlayers()
            self.assign_color_to_player(player)
            print("players {0}".format([p for p in self.players]))
    
    def DelPlayer(self, player):
        print("Deleting Player {0}".format(str(player.addr)))
        del self.players[player]
        self.SendPlayers()
    
    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
    
    def SendToAll(self, data):
        [p.Send(data) for p in self.players]
    
    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

    def player_can_write(self, player):
        return self.game_started and self._game.current_player.color == self.player_to_class[player].color

    def pick_color(self):
        choice = random.choice(self.available_classes)
        self.available_classes.remove(choice)
        return choice

    def assign_color_to_player(self, player):
        self.player_to_class[player] = self.pick_color()
        if len(self.player_to_class.values()) == 4:
            print(list(self.player_to_class.values()))
            self._game = Game(list(self.player_to_class.values()))
            self.game_started = True
        return self.player_to_class[player]

    def color_class_for_player(self, player):
        return self.player_to_class[player]

    def draw_board(self):
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
        return b

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage: {0} host:port".format(sys.argv[0]))
    print("e.g. {0} localhost:31425".format(sys.argv[0]))
else:
    host, port = sys.argv[1].split(":")
    s = ChatServer(localaddr=(host, int(port)))
    s.Launch()

