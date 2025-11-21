import math

from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtGui import QPen, QColor

from gameObjects import Bullet


class Tank:
    def __init__(self, x, y, direction, playerName):
        self.x = x
        self.y = y
        self.direction = direction
        self.playerName = playerName
        self.width = 30
        self.height = 20
        self.turretLength = 15
        self.speed = 3
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def forward(self):
        rad = math.radians(self.direction)
        self.x += self.speed * math.cos(rad)
        self.y += self.speed * math.sin(rad)

    def backward(self):
        rad = math.radians(self.direction)
        self.x -= self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)

    def left(self):
        self.direction = (self.direction - 5) % 360

    def right(self):
        self.direction = (self.direction + 5) % 360

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = 60
            bulletX = self.x
            bulletY = self.y
            bullet = Bullet(bulletX, bulletY, self.direction, self.playerName)
            return bullet

    def draw(self, painter):
        # Рисуем корпус танка
        painter.setPen(QPen(Qt.GlobalColor.red, 2))
        painter.setBrush(QColor(200, 200, 200))

        # Рисуем прямоугольник корпуса
        painter.save()
        painter.translate(self.x, self.y)
        painter.rotate(self.direction)
        painter.drawRect(-self.width // 2, -self.height // 2, self.width, self.height)

        # Рисуем башню
        painter.drawLine(0, 0, self.turretLength, 0)
        painter.restore()

    def getHitbox(self):
        hitbox = QRectF(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return hitbox
