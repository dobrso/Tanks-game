from PyQt6.QtCore import QObject, pyqtSignal


class Signals(QObject):
    roomsUpdateSignal = pyqtSignal(list)
    roomPlayersUpdateSignal = pyqtSignal(list)
    chatUpdateSignal = pyqtSignal(str)
    gameStateUpdateSignal = pyqtSignal(dict)
