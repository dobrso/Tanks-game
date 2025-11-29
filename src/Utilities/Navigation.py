class Navigation:
    def __init__(self, stackedWidget):
        self.stackedWidget = stackedWidget
        self.screens = {}

    def addScreen(self, name, screen):
        self.screens[name] = self.stackedWidget.addWidget(screen)

    def showScreen(self, name):
        if name in self.screens:
            self.stackedWidget.setCurrentIndex(self.screens[name])
