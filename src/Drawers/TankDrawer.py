import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QTransform, QColor, QPen

from src.Utilities.Settings import TANK_HULL_PATH, TANK_GUN_PATH


class TankDrawer:
    def __init__(self):
        self.isTexturesLoaded = False
        self.hullTextures = []
        self.gunTextures = []

        self.loadTextures()

    def loadTextures(self):
        if self.isTexturesLoaded:
            return

        try:
            for tankHullPath in TANK_HULL_PATH:
                if os.path.exists(tankHullPath):
                    pixmap = QPixmap(tankHullPath)
                    transform = QTransform()
                    transform.rotate(90)
                    rotatedPixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
                    self.hullTextures.append(rotatedPixmap)

            for tankGunPath in TANK_GUN_PATH:
                if os.path.exists(tankGunPath):
                    pixmap = QPixmap(tankGunPath)
                    transform = QTransform()
                    transform.rotate(90)
                    rotatedPixmap = pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
                    self.gunTextures.append(rotatedPixmap)

            self.isTexturesLoaded = True
            print("Все текстуры танков загружены успешно")

        except Exception as e:
            print(f"Ошибка загрузки текстур: {e}")

    def getTextureIndex(self, playerName):
        try:
            return int(playerName[5:]) % 4
        except:
            return 0

    def draw(self, painter, tank):
        if not self.isTexturesLoaded:
            self.drawSimpleTank(painter, tank)
        else:
            self.drawTank(painter, tank)

    def drawTank(self, painter, tank):
        textureIndex = self.getTextureIndex(tank.playerName)

        painter.save()
        painter.translate(tank.x, tank.y)
        painter.rotate(tank.direction)

        self.drawHull(painter, tank, textureIndex)

        self.drawGun(painter, tank, textureIndex)

        painter.restore()

    def drawHull(self, painter, tank, textureIndex):
        if self.hullTextures and textureIndex < len(self.hullTextures):
            hullTexture = self.hullTextures[textureIndex]
            scaledHull = hullTexture.scaled(
                tank.width, tank.height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(-tank.width // 2, -tank.height // 2, scaledHull)

    def drawGun(self, painter, tank, textureIndex):
        if self.gunTextures and textureIndex < len(self.gunTextures):
            gunTexture = self.gunTextures[textureIndex]
            gunWidth = tank.turretLength
            gunHeight = 30
            scaledGun = gunTexture.scaled(
                gunWidth, gunHeight,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            gunOffset = -tank.width // 4
            painter.drawPixmap(gunOffset, -gunHeight // 2, scaledGun)

    def drawSimpleTank(self, painter, tank):
        painter.setPen(QPen(Qt.GlobalColor.red, 2))
        painter.setBrush(QColor(200, 200, 200))

        painter.save()
        painter.translate(tank.x, tank.y)
        painter.rotate(tank.direction)
        painter.drawRect(-tank.width // 2, -tank.height // 2, tank.width, tank.height)

        painter.drawLine(0, 0, tank.turretLength, 0)
        painter.restore()

    def drawHitbox(self, painter, tank):
        hitbox = tank.getHitbox()

        oldPen = painter.pen()
        oldBrush = painter.brush()

        pen = QPen(QColor(255, 0, 0, 200))
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(QColor(255, 0, 0, 50))

        painter.drawRect(hitbox)

        painter.setPen(oldPen)
        painter.setBrush(oldBrush)
