import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform, QPen, QColor, QBrush

from src.utilities.Settings import BULLET_PATH, DEBUG_MODE


class BulletDrawer:
    def __init__(self, debugMode=DEBUG_MODE):
        self.debugMode = debugMode
        self.isTextureLoaded = False
        self.bulletTexture = None

        self.loadTexture()

    def loadTexture(self):
        if self.isTextureLoaded:
            return

        try:
            if os.path.exists(BULLET_PATH):
                pixmap = QPixmap(BULLET_PATH)
                transform = QTransform()
                transform.rotate(90)
                rotatedPixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
                self.bulletTexture = rotatedPixmap

            self.isTextureLoaded = True

        except Exception as e:
            print(f"Ошибка загрузки текстур: {e}")

    def draw(self, painter, bullet):
        if not self.isTextureLoaded or self.bulletTexture is None:
            self.drawSimpleBullet(painter, bullet)
        else:
            self.drawBullet(painter, bullet)

        if self.debugMode:
            self.drawHitbox(painter, bullet)

    def drawBullet(self, painter, bullet):
        painter.save()
        painter.translate(bullet.x, bullet.y)
        painter.rotate(bullet.direction)

        scaledBullet = self.bulletTexture.scaled(
            bullet.width,
            bullet.height,
            Qt.AspectRatioMode.IgnoreAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        painter.drawPixmap(-bullet.width // 2, -bullet.height // 2, scaledBullet)
        painter.restore()

    def drawSimpleBullet(self, painter, bullet):
        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawEllipse(int(bullet.x - bullet.width // 2), int(bullet.y - bullet.height // 2), bullet.width,
                            bullet.height)

    def drawHitbox(self, painter, bullet):
        hitbox = bullet.getHitbox()

        oldPen = painter.pen()
        oldBrush = painter.brush()

        pen = QPen(QColor(255, 0, 0, 200))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0, 50))

        painter.drawRect(hitbox)

        painter.setPen(oldPen)
        painter.setBrush(oldBrush)
