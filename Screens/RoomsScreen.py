from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem


class RoomsScreen(QWidget):
    def __init__(self, client, communication, navigation):
        super().__init__()
        self.client = client
        self.communication = communication
        self.navigation = navigation

        self.communication.roomsUpdateSignal.connect(self.updateRoomsList)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        toMenuButton = QPushButton("Назад")
        toMenuButton.clicked.connect(self.toMenuScreen)

        self.roomsList = QListWidget()

        buttonsLayout = QHBoxLayout()

        connectButton = QPushButton("Подключиться")
        connectButton.clicked.connect(self.joinRoom)

        toCreateRoomButton = QPushButton("Создать комнату")
        toCreateRoomButton.clicked.connect(self.toCreateRoomScreen)

        buttonsLayout.addWidget(connectButton)
        buttonsLayout.addWidget(toCreateRoomButton)

        layout.addWidget(toMenuButton)
        layout.addWidget(self.roomsList)
        layout.addLayout(buttonsLayout)


    def toMenuScreen(self):
        self.navigation.showScreen("menu")

    def toCreateRoomScreen(self):
        self.navigation.showScreen("createRoom")

    def joinRoom(self):
        selectedRoom = self.roomsList.currentItem()
        if selectedRoom:
            roomName = selectedRoom.text()
            self.client.currentRoom = roomName
            message = {
                "type": "join_room",
                "room_name": roomName
            }
            self.client.sendMessage(message)

            self.navigation.showScreen("game")

    def updateRoomsList(self):
        selectedRoom = self.roomsList.currentItem()
        roomName = selectedRoom.text() if selectedRoom else None

        self.roomsList.clear()

        for room in self.client.rooms:
            roomItem = QListWidgetItem(room)
            self.roomsList.addItem(roomItem)

            if room == roomName:
                roomItem.setSelected(True)
                self.roomsList.setCurrentItem(roomItem)

    def requestRooms(self):
        if self.isVisible():
            self.client.sendMessage({"type": "get_rooms"})

    def showEvent(self, event):
        super().showEvent(event)
        self.requestRooms()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.roomsList.clearSelection()
