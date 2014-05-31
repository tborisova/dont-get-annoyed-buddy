#1. forbid all player to write
#2. when player throws and moves all players have to see
#client sends to clientchannel which sends to server which sends to client
import sys
from time import sleep
from sys import stdin, exit

from PodSixNet.Connection import connection, ConnectionListener

# This example uses Python threads to manage async input from sys.stdin.
# This is so that I can receive input from the console whilst running the server.
# Don't ever do this - it's slow and ugly. (I'm doing it for simplicity's sake)
from threading import *

class Client(ConnectionListener): #client sends messages to clientchannel which is in chatserver
    def __init__(self, host, port):
        self.Connect((host, port))
        print("Chat client started")
        print("Ctrl-C to exit")
        # get a nickname from the user before starting
        print("Choose color: ")
        connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})
        # launch our threaded input loop
        t = Thread(target=self.InputLoop).start()
   # t = start_new_thread(self.InputLoop, ())
    
    def Loop(self):
        connection.Pump()
        self.Pump()
    
    def InputLoop(self):
        # horrid threaded input loop
        # continually reads from stdin and sends whatever is typed to the server
        while 1:
            #should be check if player can write
            connection.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
    
    #######################################
    ### Network event/message callbacks ###
    #######################################
    
    def Network_players(self, data):
        print("*** players: {0}".format(", ".join([p for p in data['players']])))
    
    def Network_message(self, data):
        print(data['message'])
    
    # built in stuff

    def Network_connected(self, data):
        print("You are now connected to the server")
    
    def Network_error(self, data):
        print('error:'.format(data['error'][1]))
        connection.Close()
    
    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

if len(sys.argv) != 2:
    print("Usage: {0} host:port".format(sys.argv[0]))
    print("e.g. {0} localhost:31425".sys.argv[0])
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)
