import pickle
import socket
import threading
import time

from src.Utilities.Settings import HOST, PORT, BUFFER_SIZE
from src.GameObjects.Tank import Tank


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        self.clients = {}
        self.clientsLock = threading.RLock()

        self.rooms = {}
        self.roomsLock = threading.RLock()

    def startServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        with serverSocket:
            serverSocket.bind((self.host, self.port))
            serverSocket.listen()

            print(f"[СЕРВЕР]: {self.host}:{self.port}")

            while True:
                connection, address = serverSocket.accept()

                clientHandleThread = threading.Thread(target=self.handleClient, args=(connection, address))
                clientHandleThread.start()

    def handleClient(self, connection, address):
        print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ]: {address}")

        username = f"Игрок{address[1]}"

        with self.clientsLock:
            self.clients[connection] = username

        try:
            while True:
                data = connection.recv(BUFFER_SIZE)
                if not data:
                    print(f"отключился {address}")
                    break

                message = pickle.loads(data)
                self.handleMessage(message, connection)

        except Exception as e:
            print(e)

        finally:
            with self.roomsLock:
                for roomName, roomData in self.rooms.items():
                    if connection in roomData["players"]:
                        roomData["players"].remove(connection)
                    if self.clients[connection] in roomData["tanks"]:
                        del roomData["tanks"][self.clients[connection]]
                    if not roomName:
                        del self.rooms[roomName]

            with self.clientsLock:
                if connection in self.clients:
                    del self.clients[connection]

            connection.close()

    def handleMessage(self, message, connection):
        messageType = message["type"]
        playerName = self.clients[connection]

        if messageType == "get_rooms":
            self.broadcastRooms()

        elif messageType == "create_room":
            roomName = message["room_name"]
            self.createRoom(roomName, connection, playerName)

        elif messageType == "join_room":
            roomName = message["room_name"]
            self.joinRoom(roomName, connection, playerName)

        elif messageType == "leave_room":
            roomName = message["room_name"]
            self.leaveRoom(roomName, connection, playerName)

        elif messageType == "get_players":
            roomName = message["room_name"]
            self.broadcastRoom(roomName)

        elif messageType == "send_message":
            text = message["text"]
            roomName = message["room_name"]
            self.chat(roomName, playerName, text)

        elif messageType == "player_action":
            roomName = message["room_name"]
            action = message["action"]
            self.handlePlayerAction(roomName, action, playerName)

        else:
            print("[ОШИБКА]: неизвестный тип запроса")

    def sendMessage(self, message, connection):
        try:
            message = pickle.dumps(message)
            connection.send(message)
        except Exception as e:
            print(e)

    def broadcastRooms(self):
        message: dict

        with self.roomsLock:
            message = {
                "type": "rooms",
                "rooms": list(self.rooms.keys())
            }

        with self.clientsLock:
            for client in list(self.clients.keys()):
                self.sendMessage(message, client)

        print("[ROOMS]: список комнат отправлен всем клиентам")

    def broadcastRoom(self, roomName):
        players = []

        with self.roomsLock:
            for connection in self.rooms[roomName]["players"]:
                players.append(self.clients[connection])

        message = {
            "type": "players",
            "players": players
        }

        with self.roomsLock:
            for client in self.rooms[roomName]["players"]:
                self.sendMessage(message, client)

        print(f"[ROOM]: список участников {roomName} отправлен игрокам этой комнаты")

    def createRoom(self, roomName, connection, playerName):
        with self.roomsLock:
            if roomName not in self.rooms:
                self.rooms[roomName] = {
                    "players": [connection],
                    "tanks": {},
                    "bullets": [],
                    "gameLoopThread": None
                }
                print(f"[КОМНАТА]: создана комната {roomName} игроком {playerName}")
                self.rooms[roomName]["tanks"][playerName] = Tank(200, 200, 120, playerName)
                self.broadcastRooms()
                self.startGameLoopThread(roomName)
            else:
                print(f"[ERROR]: комната с именем {roomName} уже существует")

    def joinRoom(self, roomName, connection, playerName):
        with self.roomsLock:
            if roomName in self.rooms:
                self.rooms[roomName]["players"].append(connection)
                self.rooms[roomName]["tanks"][playerName] = Tank(200, 100, 60, playerName)
                self.broadcastRoom(roomName)
                print(f"[КОМНАТА]: в {roomName} подключился {playerName}")

    def leaveRoom(self, roomName, connection, playerName):
        with self.roomsLock:
            if roomName in self.rooms:
                if connection in self.rooms[roomName]["players"]:
                    self.rooms[roomName]["players"].remove(connection)
                    self.broadcastRoom(roomName)
                if playerName in self.rooms[roomName]["tanks"]:
                    del self.rooms[roomName]["tanks"][playerName]
                    self.broadcastRoom(roomName)
                print(f"[КОМНАТА]: {playerName} покинул комнату {roomName}")

                if not self.rooms[roomName]["players"]:
                    del self.rooms[roomName]
                    self.broadcastRooms()
                    print(f"[КОМНАТА]: {roomName} была удалена")

    def chat(self, roomName, playerName, text):
        newText = f"[{playerName}]: {text}"

        message = {
            "type": "chat",
            "text": newText
        }

        with self.roomsLock:
            for client in self.rooms[roomName]["players"]:
                self.sendMessage(message, client)

        print(f"[ЧАТ]: игрок {playerName} отправил в чат {text}")

    def handlePlayerAction(self, roomName, action, playerName):
        with self.roomsLock:
            tank = self.rooms[roomName]["tanks"][playerName]

            if action == "forward":
                tank.forward()
            elif action == "backward":
                tank.backward()
            elif action == "left":
                tank.left()
            elif action == "right":
                tank.right()
            elif action == "shoot":
                bullet = tank.shoot()
                if bullet:
                    self.rooms[roomName]["bullets"].append(bullet)

    def startGameLoopThread(self, roomName):
        with self.roomsLock:
            if roomName in self.rooms:
                roomThread = self.rooms[roomName]["gameLoopThread"]
                if roomThread is None or not roomThread.is_alive():
                    roomThread = threading.Thread(target=self.gameLoop, args=(roomName, ), daemon=True)
                    roomThread.start()

    def gameLoop(self, roomName):
        while True:
            with self.roomsLock:
                if roomName not in self.rooms:
                    break

                roomData = self.rooms[roomName]

                if not roomData["players"]:
                    break

                self.checkBulletHit(roomData)

                for bullet in roomData["bullets"]:
                    bullet.update()
                    if bullet.isExpired() or bullet.isOutOfBounds():
                        roomData["bullets"].remove(bullet)

                for tank in roomData["tanks"].values():
                    tank.update()

                gameState = {"tanks": list(roomData["tanks"].values()), "bullets": roomData["bullets"]}
                message = {
                    "type": "game_state",
                    "game_state": gameState
                }

                with self.clientsLock:
                    for connection in roomData["players"]:
                        if connection in self.clients:
                                self.sendMessage(message, connection)

            time.sleep(0.016)

    def checkBulletHit(self, roomData):
        for bullet in roomData["bullets"]:
            for playerName, tank in roomData["tanks"].items():
                if bullet.playerName == playerName:
                    continue

                bulletHitbox = bullet.getHitbox()
                tankHitbox = tank.getHitbox()

                if bulletHitbox.intersects(tankHitbox):
                    roomData["bullets"].remove(bullet)
                    tank.respawn()
