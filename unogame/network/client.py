import socket
import threading
from single_play import Game
from models.button import Component
from models.Human import Human

class client(Game):
    def __init__(self, ip, screen, keys, config, soundFX):
        super().__init__(screen, keys, config, soundFX)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = ip
        self.port = 10011
        self.is_host = False       
        self.connect = True 
        
        self.info_list[1].is_empty = False
        self.info_list[1].player= Human(1, [], 1)
        self.player_number += 1
        
    def create_thread(self, target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        
    def receive_data(self):
        while True:
            data = self.sock.recv(1024).decode()
            data = data.split('-')
            print(data)        

    def main(self):
        
        print("TEST")
        try:
            print("connecting to server...")
            self.sock.connect((self.ip, self.port))
            self.create_thread(self.receive_data)
        
            self.game = Game(self.screen, self.keys, self.config, self.soundFX)
            self.game.start_single_play()
        except Exception as e:
            print(e)