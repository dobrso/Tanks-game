import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPen

from src.Utilities.Settings import BACKGROUND_PATH


class GameFieldDrawer:
    def __init__(self):
        self.isTexturesLoaded = False
        self.backgroundTextures = []

        self.loadTextures()

    def loadTextures(self):
        if self.isTexturesLoaded:
            return

        try:
            for backgroundPath in BACKGROUND_PATH:
                if os.path.exists(backgroundPath):
                    pixmap = QPixmap(backgroundPath)
                    self.backgroundTextures.append(pixmap)

            self.isTexturesLoaded = True
            print("Все текстуры фонов загружены успешно")

        except Exception as e:
            print(f"Ошибка загрузки текстур: {e}")

    def draw(self, painter, rectangle):
        self.drawBorder(painter, rectangle)

        if not self.isTexturesLoaded:
            self.drawSimpleBackground(painter, rectangle)
        else:
            self.drawBackground(painter, rectangle)

    def drawSimpleBackground(self, painter, rectangle):
        painter.fillRect(rectangle, Qt.GlobalColor.white)

    def drawBackground(self, painter, rectangle):
        painter.drawPixmap(rectangle, self.backgroundTextures[0])

    def drawBorder(self, painter, rectangle):
        oldPen = painter.pen()

        borderPen = QPen(Qt.GlobalColor.black)
        borderPen.setWidth(3)
        painter.setPen(borderPen)

        painter.drawRect(rectangle)

        painter.setPen(oldPen)