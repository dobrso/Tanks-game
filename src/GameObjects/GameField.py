from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QWidget

from src.Drawers.BulletDrawer import BulletDrawer
from src.Drawers.TankDrawer import TankDrawer


class GameField(QWidget):
    def __init__(self, client, signals):
        super().__init__()
        self.client = client
        self.signals = signals

        self.tankDrawer = TankDrawer()
        self.bulletDrawer = BulletDrawer()

        self.tanks = []
        self.bullets = []
        self.pressedKeys = set()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.signals.gameStateUpdateSignal.connect(self.updateGameState)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGame)
        self.timer.setInterval(16)

    @pyqtSlot(dict)
    def updateGameState(self, gameState):
        self.tanks = gameState["tanks"]
        self.bullets = gameState["bullets"]

    @pyqtSlot()
    def updateGame(self):
        self.handleTankInput()
        self.update()

    def handleTankInput(self):
        if not self.pressedKeys:
            return

        for key in self.pressedKeys:
            if key in ["W", "Ц"]:
                self.client.sendAction("forward")
            elif key in ["S", "Ы"]:
                self.client.sendAction("backward")
            elif key in ["A", "Ф"]:
                self.client.sendAction("left")
            elif key in ["D", "В"]:
                self.client.sendAction("right")
            elif key == "SPACE":
                self.client.sendAction("shoot")

    def keyPressEvent(self, event):
        validKeys = ["W", "S", "A", "D", "Ц", "Ы", "Ф", "В", "SPACE"]
        key = "SPACE" if event.text() == " " else event.text().upper()

        if key in validKeys:
            self.pressedKeys.add(key)

    def keyReleaseEvent(self, event):
        key = "SPACE" if event.text() == " " else event.text().upper()

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
        for tank in self.tanks:
            self.tankDrawer.draw(painter, tank)

    def drawBullets(self, painter):
        for bullet in self.bullets:
            self.bulletDrawer.draw(painter, bullet)

    def drawBorder(self, painter):
        oldPen = painter.pen()

        borderPen = QPen(Qt.GlobalColor.black)
        borderPen.setWidth(3)
        painter.setPen(borderPen)

        rect = self.rect()
        painter.drawRect(rect)

        painter.setPen(oldPen)

    def showEvent(self, event):
        super().showEvent(event)
        self.timer.start()

    def hideEvent(self, event):
        super().hideEvent(event)
        self.timer.stop()
