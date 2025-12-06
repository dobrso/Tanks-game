import math

from PyQt6.QtCore import QRectF

from src.utilities.Settings import GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT


class Bullet:
    def __init__(self, x, y, direction, playerName):
        self.x = x
        self.y = y
        self.direction = direction
        self.playerName = playerName

        self.width = 80
        self.height = 80

        self.speed = 7
        self.lifetime = 60

    def update(self):
        radians = math.radians(self.direction)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

        if self.lifetime != 0:
            self.lifetime -= 1

    def isExpired(self):
        return self.lifetime == 0

    def isOutOfBounds(self):
        return (self.x < 0 or self.x > GAME_FIELD_WIDTH or
                self.y < 0 or self.y > GAME_FIELD_HEIGHT)

    def getHitbox(self):
        hitboxWidth = self.width // 4
        hitboxHeight = self.height // 4
        hitbox = QRectF(self.x - hitboxWidth // 2, self.y - hitboxHeight // 2, hitboxWidth, hitboxHeight)
        return hitbox
