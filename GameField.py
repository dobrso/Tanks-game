from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget

from gameObjects import Tank, Bullet


class GameField(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.pressedKeys = set()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(16)

    def updateGame(self):
        self.handleTankInput()
        self.update()

    def handleTankInput(self):
        if not self.pressedKeys:
            return

        for key in self.pressedKeys:
            if key in ["W", "Ц"]:
                self.client.sendMoveAction("forward")
            elif key in ["S", "Ы"]:
                self.client.sendMoveAction("backward")
            elif key in ["A", "Ф"]:
                self.client.sendMoveAction("left")
            elif key in ["D", "В"]:
                self.client.sendMoveAction("right")
            elif key == " ":
                self.client.sendMoveAction("shoot")

    def keyPressEvent(self, event):
        validKeys = ["W", "S", "A", "D", "Ц", "Ы", "Ф", "В", " "]
        key = event.text().upper()

        if key in validKeys:
            self.pressedKeys.add(key)

    def keyReleaseEvent(self, event):
        key = event.text().upper()

        if key in self.pressedKeys:
            self.pressedKeys.remove(key)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(self.rect(), Qt.GlobalColor.white)
        self.drawBorder(painter)

        self.drawTanks(painter)
        self.drawBullets(painter)

    def drawTanks(self, painter):
        for player, tank in self.client.tanks.items():
            tank.draw(painter)

    def drawBullets(self, painter):
        for bullet in self.client.bullets:
            bullet.draw(painter)

    def drawBorder(self, painter):
        oldPen = painter.pen()

        borderPen = QPen(Qt.GlobalColor.black)
        borderPen.setWidth(3)
        painter.setPen(borderPen)

        rect = self.rect()
        painter.drawRect(rect)

        painter.setPen(oldPen)