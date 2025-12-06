from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QApplication

from src.screens.GameScreen import GameScreen
from src.screens.RoomsScreen import RoomsScreen
from src.utilities.AudioPlayer import AudioPlayer
from src.network.Client import Client
from src.utilities.Navigation import Navigation
from src.utilities.Signals import Signals
from src.utilities.Settings import WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, ICON_PATH


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setWindowIcon(QIcon(ICON_PATH))
        self.centerWindow()

        self.signals = Signals()

        self.client = Client(self.signals)
        self.client.connect()

        self.audioPlayer = AudioPlayer()
        self.audioPlayer.playMenuMusic()

        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.navigation = Navigation(self.stackedWidget)

        self.createScreens()

        self.navigation.showScreen("rooms")

    def createScreens(self):
        roomsScreen = RoomsScreen(self.client, self.signals, self.navigation)
        gameScreen = GameScreen(self.client, self.signals, self.navigation, self.audioPlayer)

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
