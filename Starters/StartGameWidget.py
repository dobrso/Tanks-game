import sys

from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import QApplication

from src.Utilities.Settings import STYLE_PATH
from src.Windows.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    style = QFile(STYLE_PATH)
    if style.open(QFile.OpenModeFlag.ReadOnly):
        stream = QTextStream(style)
        app.setStyleSheet(stream.readAll())
        style.close()

    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
