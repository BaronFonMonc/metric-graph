from matplotlib.backends.backend_qt5 import NavigationToolbar2QT


class MyToolbar(NavigationToolbar2QT):
    def __init__(self, canvas, window):
        super(MyToolbar, self).__init__(canvas, window)
        unwanted_buttons = ['Customize']
        for x in self.actions():
            if x.text() in unwanted_buttons:
                self.removeAction(x)