from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QVBoxLayout

from src.GameObjects.GameField import GameField


class GameScreen(QWidget):
    def __init__(self, client, signals, navigation, audioPlayer):
        super().__init__()
        self.client = client
        self.signals = signals
        self.navigation = navigation
        self.audioPlayer = audioPlayer

        self.signals.roomPlayersUpdateSignal.connect(self.updateRoomPlayersList)
        self.signals.chatUpdateSignal.connect(self.updateChat)

        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)

        leaveButton = QPushButton("Выйти в Лобби")
        leaveButton.setProperty("class", "danger")
        leaveButton.clicked.connect(self.leaveRoom)

        self.roomLabel = QLabel()
        self.roomLabel.setObjectName("roomLabel")
        self.roomLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.roomLabel.setProperty("class", "title")

        playersLayout = QVBoxLayout()
        playersLayout.setSpacing(8)

        playersLabel = QLabel("ИГРОКИ")
        playersLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        playersLabel.setProperty("class", "title")

        self.playersList = QTextEdit()
        self.playersList.setObjectName("playersList")
        self.playersList.setReadOnly(True)

        playersLayout.addWidget(playersLabel)
        playersLayout.addWidget(self.playersList)

        chatLayout = QVBoxLayout()
        chatLayout.setSpacing(8)

        chatLabel = QLabel("ЧАТ")
        chatLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chatLabel.setProperty("class", "title")

        self.chatField = QTextEdit()
        self.chatField.setObjectName("chatField")
        self.chatField.setReadOnly(True)

        chatLayout.addWidget(chatLabel)
        chatLayout.addWidget(self.chatField)

        self.inputField = QLineEdit()
        self.inputField.setObjectName("inputField")
        self.inputField.setPlaceholderText("Введите сообщение...")
        self.inputField.returnPressed.connect(self.sendMessageToChat)

        self.gameField = GameField(self.client, self.signals)

        layout.addWidget(leaveButton, 0, 0)
        layout.addWidget(self.roomLabel, 0, 1, 1, 3)
        layout.addLayout(playersLayout, 1, 0)
        layout.addLayout(chatLayout, 2, 0)
        layout.addWidget(self.inputField, 3, 0)
        layout.addWidget(self.gameField, 1, 1, 3, 3)

        layout.setRowStretch(1, 1)
        layout.setRowStretch(2, 3)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 2)

        self.setLayout(layout)

    @pyqtSlot()
    def leaveRoom(self):
        self.client.leaveRoom()
        self.navigation.showScreen("rooms")

    @pyqtSlot(list)
    def updateRoomPlayersList(self, newPlayersList):
        self.playersList.clear()

        for player in newPlayersList:
            self.playersList.append(player)

    @pyqtSlot()
    def sendMessageToChat(self):
        text = self.inputField.text().strip()
        if text:
            self.client.sendMessageToChat(text)
        self.inputField.clear()
        self.gameField.setFocus()

    @pyqtSlot(str)
    def updateChat(self, text):
        self.chatField.append(text)

    def setRoomLabel(self):
        roomName = self.client.currentRoom if self.client.currentRoom else "КАК ТЫ СЮДА ПОПАЛ ВАЩЕ???"
        self.roomLabel.setText(f"КОМНАТА: {roomName}")

    def requestPlayers(self):
        self.client.requestPlayers()

    def showEvent(self, event):
        super().showEvent(event)
        self.setRoomLabel()
        self.requestPlayers()
        self.chatField.clear()
        self.gameField.setFocus()
        self.audioPlayer.playMatchMusic()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.audioPlayer.playMenuMusic()
