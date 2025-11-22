import pickle
import socket
import threading

from Settings import HOST, PORT, BUFFER_SIZE


class Client(threading.Thread):
    def __init__(self, communication, host=HOST, port=PORT):
        super().__init__()
        self.communication = communication

        self.host = host
        self.port = port

        # TODO
        # Запрос с сервера на получение имени
        self.username = None

        self.currentRoom = None

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.start()

    def run(self):
        while True:
            try:
                data = self.sock.recv(BUFFER_SIZE)
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

    def sendAction(self, action):
        if self.currentRoom:
            message = {
                "type": "player_action",
                "room_name": self.currentRoom,
                "action": action
            }
            self.sendMessage(message)

    def parseMessage(self, message):
        messageType = message["type"]

        if messageType == "rooms":
            newRoomsList = message["rooms"]
            self.communication.roomsUpdateSignal.emit(newRoomsList)

        if messageType == "players":
            newPlayersList = message["players"]
            self.communication.roomPlayersUpdateSignal.emit(newPlayersList)

        if messageType == "chat":
            text = message["text"]
            self.communication.chatUpdateSignal.emit(text)

        if messageType == "game_state":
            gameState = message["game_state"]
            self.communication.gameStateUpdateSignal.emit(gameState)

    def leaveRoom(self):
        message = {
            "type": "leave_room",
            "room_name": self.currentRoom
        }
        self.currentRoom = None
        self.sendMessage(message)
