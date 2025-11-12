from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QListWidget, \
    QHBoxLayout, QLineEdit, QListWidgetItem

from Client import Client


client = Client()


class Navigation:
    def __init__(self, stackedWidget):
        self.stackedWidget = stackedWidget
        self.screens = {}

    def addScreen(self, name, screen):
        self.screens[name] = self.stackedWidget.addWidget(screen)

    def showScreen(self, name):
        if name in self.screens:
            self.stackedWidget.setCurrentIndex(self.screens[name])


class MenuScreen(QWidget):
    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation

        layout = QVBoxLayout(self)
        btn = QPushButton("Играть")
        btn.clicked.connect(self.toRooms)
        layout.addWidget(btn)

    def toRooms(self):
        client.send_command({"type": "get_rooms"})
        self.navigation.showScreen("rooms")


class RoomsScreen(QWidget):
    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation

        layout = QVBoxLayout(self)

        toMenuButton = QPushButton("Назад")
        toMenuButton.clicked.connect(self.toMenu)

        self.roomsList = QListWidget()
        self.updateRoomsList()

        buttonsLayout = QHBoxLayout()

        connectButton = QPushButton("Подключиться")
        connectButton.clicked.connect(self.joinRoom)

        toCreateRoomButton = QPushButton("Создать комнату")
        toCreateRoomButton.clicked.connect(self.toCreateRoom)

        refreshRoomsButton = QPushButton("Обновить")
        refreshRoomsButton.clicked.connect(self.updateRoomsList)

        buttonsLayout.addWidget(connectButton)
        buttonsLayout.addWidget(toCreateRoomButton)
        buttonsLayout.addWidget(refreshRoomsButton)

        layout.addWidget(toMenuButton)
        layout.addWidget(self.roomsList)
        layout.addLayout(buttonsLayout)

    def toMenu(self):
        self.navigation.showScreen("menu")

    def joinRoom(self):
        selectedRoom = self.roomsList.currentItem()
        if selectedRoom:
            pass

    def toCreateRoom(self):
        self.navigation.showScreen("createRoom")

    def updateRoomsList(self):
        self.roomsList.clear()

        for room in client.rooms:
            roomItem = QListWidgetItem(room)
            self.roomsList.addItem(roomItem)


class CreateRoomScreen(QWidget):
    def __init__(self, navigation):
        super().__init__()
        self.navigation = navigation

        layout = QVBoxLayout(self)

        toRoomsButton = QPushButton("Назад")
        toRoomsButton.clicked.connect(self.toRooms)

        self.roomNameInput = QLineEdit()
        self.roomNameInput.setPlaceholderText("Введите название комнаты")

        createButton = QPushButton("Создать")
        createButton.clicked.connect(self.createRoom)

        layout.addWidget(toRoomsButton)
        layout.addWidget(self.roomNameInput)
        layout.addWidget(createButton)

    def toRooms(self):
        client.send_command({"type": "get_rooms"})
        self.navigation.showScreen("rooms")

    def createRoom(self):
        roomName = self.roomNameInput.text().strip()
        if roomName:
            message = {
                "type": "create_room",
                "room_name": roomName
            }
            client.send_command(message)
            self.roomNameInput.clear()
