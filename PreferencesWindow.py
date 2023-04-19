from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import json
from Cloner import *
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
from typing import Callable

TIMES = ["Weekly", "Daily", "Hourly", "Minutely"]
basedir = os.path.dirname(__file__)

file_icons = QFileIconProvider()

app = QApplication([])
# Create the icon
icon = QIcon(os.path.join(basedir, "icons", "icon.png"))
# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)
menu = QMenu()
dest_tip = QAction("Destination: ")
time_tip = QAction("Time period: ")
last_time_tip = QAction("No clones yet")

def test():
    print("test")

__scheduler = BackgroundScheduler()
last_run_time = 0

def __scheduled_func(sources: list[str], dest: str):
    clone_dirs(sources, dest)
    global last_run_time
    last_run_time = int(time.time())

def start_scheduler(time_period: int, run_now: bool, sources: list[str], dest: str):
    if __scheduler.running:
        stop_scheduler()
    global last_run
    if run_now:
        __scheduled_func(sources, dest)

    if time_period == 0:
        dt = datetime.now()
        weekday = dt.weekday()
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest), trigger="cron", day_of_week=f"{weekday}", id="test")
    elif time_period == 1:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest), trigger="cron", day="1-31", id="test")
    elif time_period == 2:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest), trigger="cron", hour="0-23", id="test")
    elif time_period == 3:
        __scheduler.add_job(func=lambda: __scheduled_func(sources, dest), trigger="cron", minute="0-59", id="test")
    if __scheduler.running:
        __scheduler.resume()
    else:
        __scheduler.start()

def stop_scheduler():
    __scheduler.pause()
    __scheduler.remove_all_jobs()

class PrefsWindow(QMainWindow):

    def __init__(self, screen: QScreen):
        super().__init__()
        self.setWindowTitle("Folder Cloner Preferences")
        self.win_height = int(screen.size().height() * 0.4)
        self.win_width = int(self.win_height * 16 / 9)
        self.left = int(screen.size().width() / 2 - self.win_width / 2)
        self.top = int(screen.size().height() / 2 - self.win_height / 2)
        try:
            with open(os.path.join(basedir, "prefs.json"), "r") as f:
                self.prefs = json.load(f)
                f.close()
                global last_run_time
                last_run_time = self.prefs["last_run_time"]
        except:
            self.prefs = {
                "dest": "",
                "sources": [],
                "timer_enabled": True,
                "time_period": 2,
                "last_run_time": 0
            }
        if self.prefs["timer_enabled"] and self.prefs["dest"] != "" or len(self.prefs["sources"]) > 0:
            start_scheduler(self.prefs["time_period"], True, self.prefs["sources"], self.prefs["dest"])
            self.save_prefs()
        tray.activated.connect(self.save_prefs)
        self.__init_UI()
    
    def __init_UI(self):
        self.setWindowTitle("Folder Cloner Preferences")
        self.setGeometry(self.left, self.top, self.win_width, self.win_height)
        # --- BUTTONS ---
        # Destination selector button
        self.dest_selector = QPushButton("Select Destination")
        self.dest_selector.clicked.connect(self.select_dest)
        self.button_spacer = QLabel("")
        # Timer enable button
        self.timer_enable = QCheckBox("Scheduled clones")
        self.timer_enable.setChecked(self.prefs["timer_enabled"])
        self.timer_enable.stateChanged.connect(self.__timer_enable_changed)
        # Time period selector buttons
        self.time_period = QButtonGroup()
        self.time_buttons = [
            QRadioButton("Weekly"),
            QRadioButton("Daily"),
            QRadioButton("Hourly"),
            QRadioButton("Minutely")
        ]
        for i, button in enumerate(self.time_buttons):
            self.time_period.addButton(button, i)
            button.setEnabled(self.prefs["timer_enabled"])
            if i == self.prefs["time_period"]:
                button.setChecked(True)
        self.time_period.buttonClicked.connect(self.__time_period_changed)
        # Create the buttons layout
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.dest_selector)
        self.buttons_layout.addWidget(self.button_spacer)
        self.buttons_layout.addWidget(self.timer_enable)
        for button in self.time_buttons:
            self.buttons_layout.addWidget(button)
        self.buttons_layout.addStretch()
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)
        # --- FILENAMES ---
        # Destination label
        self.dest_label = QListWidget()
        #self.dest_label.setEnabled(False)
        # Disable scrollbar
        self.dest_label.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dest_label.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dest_label.addItem("No destination selected")
        if self.prefs["dest"] != "":
            self.dest_label.item(0).setText(self.prefs["dest"])
            self.dest_label.item(0).setIcon(file_icons.icon(QFileInfo(self.prefs["dest"])))
            # Disable selection
            self.dest_label.item(0).setFlags(Qt.ItemIsEnabled)
        h = self.dest_label.sizeHintForRow(0)
        self.dest_label.setFixedHeight(int(h*1.2))
        self.sources_label = QLabel("Sources:")
        # Source labels
        self.source_list = QListWidget()
        for source in self.prefs["sources"]:
            item = QListWidgetItem(source)
            item.setIcon(file_icons.icon(QFileInfo(source)))
            self.source_list.addItem(item)
        # Overlay add button
        self.source_add = QPushButton("+", self.source_list)
        self.source_add.clicked.connect(self.add_sources)
        self.source_add.setGeometry(0, 0, int(self.win_height/8), int(self.win_height/10))
        # Overlay remove button
        self.source_remove = QPushButton("-", self.source_list)
        self.source_remove.clicked.connect(self.remove_sources)
        self.source_remove.setGeometry(0, 0, int(self.win_height/8), int(self.win_height/10))
        self.source_remove.setEnabled(False)
        # Move the source buttons to the bottom right when the source list is resized
        self.source_list.resizeEvent = self.__move_source_buttons
        self.source_list.mouseReleaseEvent = self.__source_list_mouse_release
        # Create the filenames layout
        self.filenames_layout = QVBoxLayout()
        self.filenames_layout.addWidget(self.dest_label)
        self.filenames_layout.addWidget(self.sources_label)
        self.filenames_layout.addWidget(self.source_list)
        self.filenames_widget = QWidget()
        self.filenames_widget.setLayout(self.filenames_layout)
        # --- MAIN ---
        # Create the main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.buttons_widget)
        self.main_layout.addWidget(self.filenames_widget)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def __timer_enable_changed(self, state: int):
        self.prefs["timer_enabled"] = state == Qt.Checked
        for button in self.time_buttons:
            button.setEnabled(state == Qt.Checked)
        if state == Qt.Checked and self.prefs["dest"] != "" or len(self.prefs["sources"]) > 0:
            start_scheduler(self.prefs["time_period"], True, self.prefs["sources"], self.prefs["dest"])
        else:
            stop_scheduler()
        self.save_prefs()

    def __time_period_changed(self, button: QRadioButton):
        self.prefs["time_period"] = self.time_period.id(button)
        if self.prefs["timer_enabled"] and self.prefs["dest"] != "" or len(self.prefs["sources"]) > 0:
            start_scheduler(self.prefs["time_period"], True, self.prefs["sources"], self.prefs["dest"])
        self.save_prefs()

    def __move_source_buttons(self, event: QResizeEvent):
        add_x = event.size().width() - self.source_add.width()
        add_y = event.size().height() - self.source_add.height()
        self.source_add.move(add_x, add_y)
        remove_x = event.size().width() - self.source_remove.width() - self.source_add.width()
        remove_y = event.size().height() - self.source_remove.height()
        self.source_remove.move(remove_x, remove_y)

    def __source_list_mouse_release(self, event: QMouseEvent):
        if len(self.source_list.selectedItems()) > 0:
            item = self.source_list.indexAt(event.pos())
            if not item.isValid() or event.button() == Qt.RightButton:
                self.source_list.clearSelection()
                self.source_remove.setEnabled(False)
            else:
                self.source_remove.setEnabled(True)

    def save_prefs(self):
        with open(os.path.join(basedir, "prefs.json"), "w") as f:
            self.prefs["last_run_time"] = last_run_time
            json.dump(self.prefs, f)
            f.close()
            self.update_menu()
    
    def select_dest(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.DirectoryOnly)
        file_dialog.setDirectory(os.path.expanduser('~'))
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # Make it possible to select multiple files and directories
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.SingleSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.SingleSelection)

        if file_dialog.exec():
            paths = file_dialog.selectedFiles()
            self.prefs["dest"] = paths[0]
            self.dest_label.item(0).setText(self.prefs["dest"])
            self.dest_label.item(0).setIcon(file_icons.icon(QFileInfo(self.prefs["dest"])))
            self.save_prefs()
    
    def add_sources(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.Directory)
        file_dialog.setDirectory(os.path.expanduser('~'))
        file_dialog.setOption(QFileDialog.DontUseNativeDialog, True)
        file_view = file_dialog.findChild(QListView, 'listView')

        # Make it possible to select multiple files and directories
        if file_view:
            file_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        f_tree_view = file_dialog.findChild(QTreeView)
        if f_tree_view:
            f_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        if file_dialog.exec():
            paths = file_dialog.selectedFiles()
            for path in paths:
                if path not in self.prefs["sources"]:
                    self.prefs["sources"].append(path)
                    item = QListWidgetItem(path)
                    item.setIcon(file_icons.icon(QFileInfo(path)))
                    self.source_list.addItem(item)
            self.save_prefs()
    
    def remove_sources(self):
        for item in self.source_list.selectedItems():
            try:
                self.prefs["sources"].remove(item.text())
                self.source_list.takeItem(self.source_list.row(item))
            except ValueError:
                pass
        self.save_prefs()
    
    def limit_string(self, string: str, length: int):
        if len(string) > length:
            return "..." + string[-(length - 3):]
        else:
            return string

    def update_menu(self):
        if self.prefs["dest"] == "":
            dest_tip.setText("Destination: None")
            dest_tip.setIcon(QIcon())
        else:
            dest_tip.setText("Destination: " + self.limit_string(self.prefs["dest"], 40))
            dest_tip.setIcon(file_icons.icon(QFileInfo(self.prefs["dest"])))
        if self.prefs["timer_enabled"]:
            time_tip.setText("Scheduled clones: " + TIMES[self.prefs["time_period"]])
        else:
            time_tip.setText("Scheduled clones disabled")
        if self.prefs["last_run_time"] == 0:
            last_time_tip.setText("No clones yet")
        else:
            last_time_tip.setText("Last clone: " + time.strftime("%l:%M %p, %b %d, %Y", time.localtime(self.prefs["last_run_time"])))
    
    def run_clone(self):
        if self.prefs["dest"] == "" or len(self.prefs["sources"]) == 0:
            return
        clone_dirs(self.prefs["sources"], self.prefs["dest"])
        global last_run_time
        last_run_time = int(time.time())
        self.save_prefs()

prefs = PrefsWindow(app.primaryScreen())