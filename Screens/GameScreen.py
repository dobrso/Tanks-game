from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QListWidget, QTextEdit, QLineEdit, \
    QVBoxLayout

from GameField import GameField
from Settings import MUSIC_PATH


class GameScreen(QWidget):
    def __init__(self, client, communication, navigation, audioPlayer):
        super().__init__()
        self.client = client
        self.communication = communication
        self.navigation = navigation
        self.audioPlayer = audioPlayer

        self.communication.roomPlayersUpdateSignal.connect(self.updateRoomPlayersList)
        self.communication.chatUpdateSignal.connect(self.updateChat)

        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        leaveButton = QPushButton("Выйти")
        leaveButton.clicked.connect(self.leaveRoom)

        self.roomLabel = QLabel()
        self.roomLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        playersLayout = QVBoxLayout()

        playersLabel = QLabel("ИГРОКИ")
        playersLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.playersList = QListWidget()

        playersLayout.addWidget(playersLabel)
        playersLayout.addWidget(self.playersList)

        chatLayout = QVBoxLayout()

        chatLabel = QLabel("ЧАТ")
        chatLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.chatField = QTextEdit()
        self.chatField.setReadOnly(True)

        chatLayout.addWidget(chatLabel)
        chatLayout.addWidget(self.chatField)

        self.inputField = QLineEdit()
        self.inputField.returnPressed.connect(self.sendMessageToChat)

        self.gameField = GameField(self.client)

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

    def leaveRoom(self):
        roomName = self.client.currentRoom
        self.client.sendMessage({
            "type": "leave_room",
            "room_name": roomName
        })
        self.navigation.showScreen("rooms")

    def requestPlayers(self):
        if self.isVisible():
            message = {
                "type": "get_players",
                "room_name": self.client.currentRoom
            }
            self.client.sendMessage(message)

    def updateRoomPlayersList(self):
        self.playersList.clear()

        for player in self.client.currentRoomPlayers:
            self.playersList.addItem(player)

    def sendMessageToChat(self):
        text = self.inputField.text().strip()
        if text:
            message = {
                "type": "send_message",
                "text": text,
                "room_name": self.client.currentRoom
            }
            self.client.sendMessage(message)
        self.inputField.clear()

    def updateChat(self, text):
        self.chatField.append(text)

    def setRoomLabel(self):
        roomName = self.client.currentRoom if self.client.currentRoom else "КАК ТЫ СЮДА ПОПАЛ ВАЩЕ???"
        self.roomLabel.setText(f"КОМНАТА: {roomName}")

    def showEvent(self, event):
        super().showEvent(event)
        self.setRoomLabel()
        self.requestPlayers()
        self.chatField.clear()
        self.gameField.setFocus()
        self.audioPlayer.playMusic(MUSIC_PATH["MATCH"])

    def hideEvent(self, event):
        super().hideEvent(event)
        self.audioPlayer.playMusic(MUSIC_PATH["MENU"])
