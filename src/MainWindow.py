from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

from src.Screens.GameScreen import GameScreen
from src.Screens.MenuScreen import MenuScreen
from src.Screens.Navigation import Navigation
from src.Screens.RoomsScreen import RoomsScreen
from src.Utilities.AudioPlayer import AudioPlayer
from src.Network.Client import Client
from src.Utilities.Signals import Signals
from src.Utilities.Settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, MUSIC_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.centerWindow()

        self.signals = Signals()
        self.client = Client(self.signals)

        self.audioPlayer = AudioPlayer()
        self.audioPlayer.playMusic(MUSIC_PATH["MENU"])

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.navigation = Navigation(self.stackedWidget)

        self.createScreens()

        self.navigation.showScreen("menu")

    def createScreens(self):
        menuScreen = MenuScreen(self.client, self.navigation)
        roomsScreen = RoomsScreen(self.client, self.signals, self.navigation)
        gameScreen = GameScreen(self.client, self.signals, self.navigation, self.audioPlayer)

        self.navigation.addScreen("menu", menuScreen)
        self.navigation.addScreen("rooms", roomsScreen)
        self.navigation.addScreen("game", gameScreen)

    def centerWindow(self):
        screen = QApplication.primaryScreen()
        screenGeometry = screen.availableGeometry()

        windowGeometry = self.frameGeometry()

        centerPoint = screenGeometry.center()

        windowGeometry.moveCenter(centerPoint)

        self.move(windowGeometry.topLeft())

    def closeEvent(self, event):
        super().closeEvent(event)
        self.client.disconnect()
