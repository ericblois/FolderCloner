from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PreferencesWindow import *

app = QApplication([])
prefs = PrefsWindow(app.primaryScreen())

def display_preferences():
    prefs.show()
    prefs.raise_()

if __name__ == '__main__':
    app.setApplicationName("Folder Cloner")
    app.setApplicationDisplayName("Folder Cloner")
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("icon.png")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    action = QAction("Preferences...")
    action.triggered.connect(display_preferences)
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    app.exec()
