import pickle
import socket
import threading

from Settings import HOST, PORT


class Client(threading.Thread):
    def __init__(self, communication, host=HOST, port=PORT):
        super().__init__()
        self.communication = communication
        self.host = host
        self.port = port
        self.rooms = []

        self.currentRoom = None
        self.currentRoomPlayers = []

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.start()

    def run(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break

                message = pickle.loads(data)
                self.parseMessage(message)

            finally:
                pass

    def sendMessage(self, message):
        try:
            message = pickle.dumps(message)
            self.sock.send(message)
        except Exception as e:
            print(e)

    def parseMessage(self, message):
        messageType = message["type"]

        if messageType == "rooms":
            self.rooms = message["rooms"]
            self.communication.roomsUpdateSignal.emit()

        if messageType == "players":
            self.currentRoomPlayers = message["players"]
            self.communication.roomPlayersUpdateSignal.emit()

        if messageType == "chat":
            text = message["text"]
            self.communication.chatUpdateSignal.emit(text)
