from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class MenuScreen(QWidget):
    def __init__(self, client, navigation):
        super().__init__()
        self.client = client
        self.navigation = navigation
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        btn = QPushButton("Играть")
        btn.clicked.connect(self.toRooms)
        layout.addWidget(btn)

    def toRooms(self):
        self.navigation.showScreen("rooms")