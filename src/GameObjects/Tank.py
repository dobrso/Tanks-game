import math
import random

from PyQt6.QtCore import QRectF

from src.GameObjects.Bullet import Bullet
from src.Utilities.Settings import GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT


class Tank:
    def __init__(self, x, y, direction, playerName):
        self.x = x
        self.y = y
        self.direction = direction
        self.playerName = playerName

        self.width = 60
        self.height = 70

        self.turretLength = 50
        self.bulletOffset = 10

        self.rotationAngle = 3
        self.speed = 3
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def forward(self):
        radians = math.radians(self.direction)
        self.x += self.speed * math.cos(radians)
        self.y += self.speed * math.sin(radians)

        self.x = min(max(self.width // 2, self.x), GAME_FIELD_WIDTH - self.width // 2)
        self.y = min(max(self.height // 2, self.y), GAME_FIELD_HEIGHT - self.height // 2)

    def backward(self):
        radians = math.radians(self.direction)
        self.x -= self.speed * math.cos(radians)
        self.y -= self.speed * math.sin(radians)

        self.x = min(max(self.width // 2, self.x), GAME_FIELD_WIDTH - self.width // 2)
        self.y = min(max(self.height // 2, self.y), GAME_FIELD_HEIGHT - self.height // 2)

    def left(self):
        self.direction = (self.direction - self.rotationAngle) % 360

    def right(self):
        self.direction = (self.direction + self.rotationAngle) % 360

    def shoot(self):
        if self.cooldown == 0:
            self.cooldown = 60
            radians = math.radians(self.direction)
            bulletX = self.x + (self.turretLength - self.bulletOffset) * math.cos(radians)
            bulletY = self.y + (self.turretLength - self.bulletOffset) * math.sin(radians)
            bullet = Bullet(bulletX, bulletY, self.direction, self.playerName)
            return bullet

    def respawn(self):
        self.x = random.randint(self.width // 2, GAME_FIELD_WIDTH - self.width // 2)
        self.y = random.randint(self.height // 2, GAME_FIELD_HEIGHT - self.height // 2)
        self.direction = random.randint(0, 360)

    def getHitbox(self):
        hitbox = QRectF(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        return hitbox
