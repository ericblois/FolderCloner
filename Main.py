from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PreferencesWindow import *

# Create the menu

def display_preferences():
    prefs.show()
    prefs.raise_()

if __name__ == '__main__':
    app.setApplicationName("Folder Cloner")
    app.setApplicationDisplayName("Folder Cloner")
    app.setQuitOnLastWindowClosed(False)
    
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
    last_time_tip.setEnabled(False)
    menu.addAction(last_time_tip)
    prefs.update_menu()
    menu.addSeparator()
    # Add a Clone option to the menu
    clone = QAction("Clone folders now")
    clone.triggered.connect(prefs.run_clone)
    menu.addAction(clone)
    clone.setIcon(icon)
    # Add a Preferences option to the menu.
    preferences = QAction("Preferences")
    preferences.triggered.connect(display_preferences)
    menu.addAction(preferences)
    preferences.setIcon(QIcon(os.path.join(basedir, "icons", "gear.png")))

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)
    quit.setIcon(QIcon(os.path.join(basedir, "icons", "power.png")))

    # Add the menu to the tray
    tray.setContextMenu(menu)
    app.exec()
