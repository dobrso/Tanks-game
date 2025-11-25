from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton


class MenuScreen(QWidget):
    def __init__(self, client, navigation):
        super().__init__()
        self.client = client
        self.navigation = navigation
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        btn = QPushButton("Играть")
        btn.clicked.connect(lambda: self.navigation.showScreen("rooms"))
        layout.addWidget(btn)

        self.setLayout(layout)