import math

from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QPen, QBrush, QColor


class Bullet:
    def __init__(self, x, y, direction, playerName):
        self.x = x
        self.y = y
        self.direction = direction
        self.playerName = playerName
        self.speed = 7
        self.width = 5
        self.height = 3

    def move(self):
        rad = math.radians(self.direction)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

    def draw(self, painter):
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawEllipse(int(self.x - self.width // 2), int(self.y - self.height // 2),
                            self.width, self.height)

    def getHitbox(self):
        hitbox = QRectF(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return hitbox
