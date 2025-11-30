from PyQt6.QtCore import pyqtSlot, Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QListWidgetItem, QDialog, \
    QLineEdit, QDialogButtonBox, QLabel

from src.Utilities.Settings import WINDOW_TITLE, DIALOG_WIDTH, DIALOG_HEIGHT


class RoomsScreen(QWidget):
    def __init__(self, client, signals, navigation):
        super().__init__()
        self.client = client
        self.signals = signals
        self.navigation = navigation

        self.signals.roomsUpdateSignal.connect(self.updateRoomsList)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        roomsLabel = QLabel("Лобби")
        roomsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        roomsLabel.setProperty("class", "title")

        self.roomsList = QListWidget()
        self.roomsList.doubleClicked.connect(self.joinRoom)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setSpacing(10)

        connectButton = QPushButton("Подключиться")
        connectButton.setProperty("class", "primary")
        connectButton.clicked.connect(self.joinRoom)

        toCreateRoomButton = QPushButton("Создать комнату")
        toCreateRoomButton.clicked.connect(self.showCreateRoomDialog)

        buttonsLayout.addWidget(connectButton)
        buttonsLayout.addWidget(toCreateRoomButton)

        layout.addWidget(roomsLabel)
        layout.addWidget(self.roomsList)
        layout.addLayout(buttonsLayout)

        self.setLayout(layout)

    @pyqtSlot()
    def joinRoom(self):
        selectedRoom = self.roomsList.currentItem()
        if selectedRoom:
            roomName = selectedRoom.text()
            self.client.joinRoom(roomName)
            self.navigation.showScreen("game")

    @pyqtSlot(list)
    def updateRoomsList(self, newRoomsList):
        selectedRoom = self.roomsList.currentItem()
        roomName = selectedRoom.text() if selectedRoom else None

        self.roomsList.clear()

        for room in newRoomsList:
            roomItem = QListWidgetItem(room)
            self.roomsList.addItem(roomItem)

            if room == roomName:
                roomItem.setSelected(True)
                self.roomsList.setCurrentItem(roomItem)

    def requestRooms(self):
        if self.isVisible():
            self.client.requestRooms()

    @pyqtSlot()
    def showCreateRoomDialog(self):
        dialog = CreateRoomDialog(self)

        if dialog.exec():
            roomName = dialog.getRoomName()
            if roomName:
                self.client.createRoom(roomName)
                self.navigation.showScreen("game")

    def showEvent(self, event):
        super().showEvent(event)
        self.requestRooms()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.roomsList.clearSelection()


class CreateRoomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(DIALOG_WIDTH, DIALOG_HEIGHT)
        self.setModal(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        label = QLabel("Создание комнаты")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty("class", "title")

        self.roomNameInput = QLineEdit()
        self.roomNameInput.setPlaceholderText("Введите название комнаты")

        buttonBox = QDialogButtonBox()

        createButton = QPushButton("Создать")
        createButton.setProperty("class", "primary")
        backButton = QPushButton("Закрыть")

        buttonBox.addButton(createButton, QDialogButtonBox.ButtonRole.AcceptRole)
        buttonBox.addButton(backButton, QDialogButtonBox.ButtonRole.RejectRole)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(label)
        layout.addWidget(self.roomNameInput)
        layout.addWidget(buttonBox)

        self.setLayout(layout)

    def getRoomName(self):
        roomName = self.roomNameInput.text().strip()
        return roomName
