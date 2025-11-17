from PyQt6.QtCore import QObject, pyqtSignal


class Communication(QObject):
    roomsUpdateSignal = pyqtSignal()
    roomPlayersUpdateSignal = pyqtSignal()
    chatUpdateSignal = pyqtSignal(str)
