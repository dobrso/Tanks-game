import sys

from PyQt6.QtWidgets import QApplication

from src.Windows.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
