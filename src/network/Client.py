import pickle
import socket
import threading

from src.utilities.Settings import HOST, PORT, BUFFER_SIZE


class Client(threading.Thread):
    def __init__(self, signals, host=HOST, port=PORT):
        super().__init__()
        self.signals = signals

        self.host = host
        self.port = port

        self.socket = None
        self.running = False

        self.currentRoom = None

    def run(self):
        while self.running:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                if not data:
                    break

                message = pickle.loads(data)
                self.handleMessage(message)

            except Exception as e:
                print(f"[ОШИБКА]: {e}")

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))

            self.running = True

            self.start()
        except Exception as e:
            print(e)

    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()

    def handleMessage(self, message):
        messageType = message["type"]

        if messageType == "rooms":
            newRoomsList = message["rooms"]
            self.signals.roomsUpdateSignal.emit(newRoomsList)

        if messageType == "players":
            newPlayersList = message["players"]
            self.signals.roomPlayersUpdateSignal.emit(newPlayersList)

        if messageType == "chat":
            text = message["text"]
            self.signals.chatUpdateSignal.emit(text)

        if messageType == "game_state":
            newGameState = message["game_state"]
            self.signals.gameStateUpdateSignal.emit(newGameState)

    def sendMessage(self, message):
        try:
            message = pickle.dumps(message)
            self.socket.send(message)
        except Exception as e:
            print(e)

    def createRoom(self, roomName):
        message = {
            "type": "create_room",
            "room_name": roomName
        }
        self.currentRoom = roomName
        self.sendMessage(message)

    def joinRoom(self, roomName):
        message = {
            "type": "join_room",
            "room_name": roomName
        }
        self.currentRoom = roomName
        self.sendMessage(message)

    def leaveRoom(self):
        if self.currentRoom:
            message = {
                "type": "leave_room",
                "room_name": self.currentRoom
            }
            self.currentRoom = None
            self.sendMessage(message)

    def sendMessageToChat(self, text):
        if self.currentRoom:
            message = {
                "type": "send_message",
                "text": text,
                "room_name": self.currentRoom
            }
            self.sendMessage(message)

    def sendAction(self, action):
        if self.currentRoom:
            message = {
                "type": "player_action",
                "room_name": self.currentRoom,
                "action": action
            }
            self.sendMessage(message)

    def requestRooms(self):
        message = {
            "type": "get_rooms"
        }
        self.sendMessage(message)

    def requestPlayers(self):
        message = {
            "type": "get_players",
            "room_name": self.currentRoom
        }
        self.sendMessage(message)
