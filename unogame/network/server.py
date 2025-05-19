import socket
import threading
import pickle
from single_play import Game

class server(Game):
    def __init__(self, is_password, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)
        self.player_num = 0 
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 10011
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       
        self.conn, self.addr = None, None
        self.connection_established = False 
        self.is_host = True
        self.is_password = is_password
        
        
    def create_thread(self,target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        
    def waiting_for_connection(self):
        self.conn, self.addr = self.sock.accept()
        print("Connection from: ", self.addr)
        self.connection_established = True
        self.create_thread(self.receive_data)        
        
    def receive_data(self):
        while True:
            data = self.conn.recv(1024).decode()
            print(data)
        
    def main(self):
        self.sock.bind((self.host, self.port))
        print("Server IP: ", self.host)
        self.sock.listen(1)
        print("Waiting for connection...")
        self.create_thread(self.waiting_for_connection)
        self.game = Game(self.screen, self.keys, self.config, self.soundFX)
        self.game.start_single_play()
        
    def appendPlayer(self, player):
        self.players.append(player)
        
    def removePlayer(self, player):
        self.players.remove(player)
        