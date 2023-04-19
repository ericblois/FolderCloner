from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PreferencesWindow import *

prefs = PrefsWindow(app.primaryScreen())
# Create the menu

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
    
    # Add a title to the menu
    title = QAction("Folder Cloner is running in the background")
    title.setEnabled(False)
    menu.addAction(title)
    # Add a separator to the menu
    menu.addSeparator()
    # Add information to the menu
    dest_tip.setEnabled(False)
    menu.addAction(dest_tip)
    time_tip.setEnabled(False)
    menu.addAction(time_tip)
    prefs.update_menu()
    menu.addSeparator()
    # Add a Preferences option to the menu.
    preferences = QAction("Preferences")
    preferences.triggered.connect(display_preferences)
    menu.addAction(preferences)
    preferences.setIcon(QIcon("gear.png"))

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    quit.setIcon(QIcon("power.png"))

    # Add the menu to the tray
    tray.setContextMenu(menu)
    app.exec()
