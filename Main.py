import sys

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

from AudioPlayer import AudioPlayer
from Screens import Navigation, MenuScreen, RoomsScreen, CreateRoomScreen
from settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, MUSIC_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.audioPlayer = AudioPlayer()
        self.audioPlayer.playMusic(MUSIC_PATH["MENU"])

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.navigation = Navigation(self.stackedWidget)

        self.createScreen()

        self.navigation.showScreen("menu")

    def createScreen(self):
        menuScreen = MenuScreen(self.navigation)
        roomsScreen = RoomsScreen(self.navigation)
        createRoomScreen = CreateRoomScreen(self.navigation)

        self.navigation.addScreen("menu", menuScreen)
        self.navigation.addScreen("rooms", roomsScreen)
        self.navigation.addScreen("createRoom", createRoomScreen)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()