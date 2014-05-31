import sys
from time import sleep, localtime
from weakref import WeakKeyDictionary
from cli import CLI
from player import Player

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

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

class ClientChannel(Channel, Player):
    """
    This is the server representation of a single connected client.
    """
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)
    
    def Close(self):
        self._server.DelPlayer(self)
    
    ##################################
    ### Network specific callbacks ###
    ##################################
    
    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": BOARD})
    
    def Network_nickname(self, data):
        self.nickname = data['nickname']
        self._server.SendPlayers()

class ChatServer(Server): #CLI cli sends messages to all
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = WeakKeyDictionary()
        print('Server launched')
    
    def Connected(self, channel, addr):
        self.AddPlayer(channel)
    
    def AddPlayer(self, player):
        print("New Player {0}".format(str(player.addr)))
        self.players[player] = True
        self.SendPlayers()
        if len(self.players) == 2:
            print("will start")
            self._cli = CLI(RedPlayer([RedPlayer(), BluePlayer()]))
        print("players {0}".format([p for p in self.players]))
    
    def DelPlayer(self, player):
        print("Deleting Player {0}".format(str(player.addr)))
        del self.players[player]
        self.SendPlayers()

    def SendPlayers(self):
        self.SendToAll({"action": "players", "players": [p.nickname for p in self.players]})
    
    def SendToAll(self, data): #sends data to all players
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage: {0} host:port".format(sys.argv[0]))
    print("e.g. {0} localhost:31425".format(sys.argv[0]))
else:
    host, port = sys.argv[1].split(":")
    s = ChatServer(localaddr=(host, int(port)))
    s.Launch()

