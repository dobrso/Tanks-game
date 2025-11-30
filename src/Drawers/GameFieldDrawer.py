import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPen

from src.Utilities.Settings import BACKGROUND_PATH


class GameFieldDrawer:
    def __init__(self):
        self.isTextureLoaded = False
        self.backgroundTexture = None

        self.loadTexture()

    def loadTexture(self):
        if self.isTextureLoaded:
            return

        try:
            if os.path.exists(BACKGROUND_PATH):
                pixmap = QPixmap(BACKGROUND_PATH)
                self.backgroundTexture = pixmap

            self.isTextureLoaded = True

        except Exception as e:
            print(f"Ошибка загрузки текстур: {e}")

    def draw(self, painter, rectangle):
        self.drawBorder(painter, rectangle)

        if not self.isTextureLoaded or self.backgroundTexture is None:
            self.drawSimpleBackground(painter, rectangle)
        else:
            self.drawBackground(painter, rectangle)

    def drawSimpleBackground(self, painter, rectangle):
        painter.fillRect(rectangle, Qt.GlobalColor.white)

    def drawBackground(self, painter, rectangle):
        painter.drawPixmap(rectangle, self.backgroundTexture)

    def drawBorder(self, painter, rectangle):
        oldPen = painter.pen()

        borderPen = QPen(Qt.GlobalColor.black)
        borderPen.setWidth(3)
        painter.setPen(borderPen)

        painter.drawRect(rectangle)

        painter.setPen(oldPen)
