import sys

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

from AudioPlayer import AudioPlayer
from Client import Client
from Communication import Communication
from Screens import MenuScreen, RoomsScreen, GameScreen, Navigation
from Settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, MUSIC_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.communication = Communication()
        self.client = Client(self.communication)

        self.audioPlayer = AudioPlayer()
        self.audioPlayer.playMusic(MUSIC_PATH["MENU"])

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.navigation = Navigation(self.stackedWidget)

        self.createScreens()

        self.navigation.showScreen("menu")

        self.show()

    def createScreens(self):
        menuScreen = MenuScreen(self.client, self.navigation)
        roomsScreen = RoomsScreen(self.client, self.communication, self.navigation)
        gameScreen = GameScreen(self.client, self.communication, self.navigation, self.audioPlayer)

        self.navigation.addScreen("menu", menuScreen)
        self.navigation.addScreen("rooms", roomsScreen)
        self.navigation.addScreen("game", gameScreen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    app.exec()
