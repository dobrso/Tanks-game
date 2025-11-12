import pickle
import socket
import threading

from settings import HOST, PORT

clients = []
clientsLock = threading.Lock()

rooms = []
roomsLock = threading.Lock()

def parseMessage(message):
    messageType = message["type"]

    if messageType == "create_room":
        roomName = message["room_name"]
        with roomsLock:
            rooms.append(roomName)

        print(f"[КОМНАТА]: создана комната {roomName}")

    if messageType == "get_rooms":
        message = {}

        with roomsLock:
            message = pickle.dumps({
                "type": "rooms",
                "rooms": rooms
            })

        with clientsLock:
            for client in clients:
                client.send(message)

        print("[КОМНАТА]: отправлены комнаты клиентам")

def handleClient(conn, addr):
    print(f"НОВОЕ ПОДКЛЮЧЕНИЕ {addr}")

    with clientsLock:
        clients.append(conn)

    try:
        while True:
            message = pickle.loads(conn.recv(1024))
            if not message:
                break

            parseMessage(message)

    finally:
        with clientsLock:
            if conn in clients:
                clients.remove(conn)

        conn.close()


def startServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    with serverSocket:
        serverSocket.bind((HOST, PORT))
        serverSocket.listen()

        print("Сервер запущен")

        while True:
            conn, addr = serverSocket.accept()
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.start()


if __name__ == '__main__':
    startServer()
