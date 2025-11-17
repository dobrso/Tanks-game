from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit


class CreateRoomScreen(QWidget):
    def __init__(self, client, communication, navigation):
        super().__init__()
        self.client = client
        self.communication = communication
        self.navigation = navigation
        self.initUI()

    def initUI(self):
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
        self.navigation.showScreen("rooms")

    def createRoom(self):
        roomName = self.roomNameInput.text().strip()
        if roomName:
            self.client.currentRoom = roomName
            message = {
                "type": "create_room",
                "room_name": roomName
            }
            self.client.sendMessage(message)
            self.navigation.showScreen("game")
        self.roomNameInput.clear()