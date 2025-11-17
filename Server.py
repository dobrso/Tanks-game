import pickle
import socket
import threading

from Settings import HOST, PORT

class Server:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

        self.clients = {}
        self.clientsLock = threading.Lock()

        self.rooms = {}
        self.roomsLock = threading.Lock()

        self.startServer()

    def startServer(self):
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        with serverSocket:
            serverSocket.bind((self.host, self.port))
            serverSocket.listen()

            print(f"[СЕРВЕР РАБОТАЕТ]: {self.host}:{self.port}")

            while True:
                conn, addr = serverSocket.accept()
                clientHandler = threading.Thread(target=self.handleClient, args=(conn, addr))
                clientHandler.start()

    def handleClient(self, conn, addr):
        print(f"[НОВОЕ ПОДКЛЮЧЕНИЕ]: {addr}")

        username = f"User{addr[1]}"

        with self.clientsLock:
            self.clients[conn] = username

        try:
            while True:
                data = conn.recv(4096)
                if not data:
                    print(f"отключился {addr}")
                    break

                message = pickle.loads(data)
                self.parseMessage(message, conn)

        finally:
            with self.clientsLock:
                if conn in self.clients:
                    del self.clients[conn]

            conn.close()

    def parseMessage(self, message, conn):
        print(message)
        messageType = message["type"]
        playerName = self.clients[conn]

        if messageType == "get_rooms":
            self.sendRooms()

        elif messageType == "create_room":
            roomName = message["room_name"]
            with self.roomsLock:
                self.rooms[roomName] = [conn]

            print(f"[КОМНАТА]: создана комната {roomName} игроком {playerName}")

            self.sendRooms()

        elif messageType == "join_room":
            roomName = message["room_name"]

            with self.roomsLock:
                if roomName in self.rooms:
                    self.rooms[roomName].append(conn)

                    print(f"[КОМНАТА]: в {roomName} подключился {playerName}")

        elif messageType == "leave_room":
            roomName = message["room_name"]
            with self.roomsLock:
                if roomName in self.rooms and conn in self.rooms[roomName]:
                    self.rooms[roomName].remove(conn)
                    print(f"[КОМНАТА]: {playerName} покинул комнату {roomName}")

                if not self.rooms[roomName]:
                    del self.rooms[roomName]
                    print(f"[КОМНАТА]: {roomName} была удалена")

        elif messageType == "get_players":
            roomName = message["room_name"]
            players = []

            with self.roomsLock and self.clientsLock:
                for conn in self.rooms[roomName]:
                    players.append(self.clients[conn])

            message = pickle.dumps({
                "type": "players",
                "players": players
            })

            with self.clientsLock:
                for client in self.clients:
                    client.send(message)

        elif messageType == "send_message":
            text = message["text"]
            newText = f"[{self.clients[conn]}]: {text}"
            roomName = message["room_name"]

            message = pickle.dumps({
                "type": "chat",
                "text": newText
            })

            room = []
            with self.roomsLock:
                room = self.rooms[roomName]

            with self.clientsLock:
                for client in room:
                    client.send(message)

        else:
            print("[ОШИБКА]: неизвестный тип запроса")

    def sendRooms(self):
        message: bytes

        with self.roomsLock:
            message = pickle.dumps({
                "type": "rooms",
                "rooms": list(self.rooms.keys())
            })

        with self.clientsLock:
            for client in self.clients:
                client.send(message)

        print("[]: список комнат отправлен всем клиентам")

if __name__ == '__main__':
    server = Server()
