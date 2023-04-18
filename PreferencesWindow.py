from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

class PrefsWindow(QMainWindow):

    def __init__(self, screen: QScreen):
        super().__init__()
        self.setWindowTitle("Folder Cloner Preferences")
        self.win_width = int(screen.size().width() * 0.4)
        self.win_height = int(screen.size().height() * 0.4)
        self.left = int(screen.size().width() / 2 - self.win_width / 2)
        self.top = int(screen.size().height() / 2 - self.win_height / 2)
        self.__init_UI()
    
    def __init_UI(self):
        self.setWindowTitle("Folder Cloner Preferences")
        self.setGeometry(self.left, self.top, self.win_width, self.win_height)
        # Create the selector buttons
        self.dest_selector = QPushButton("Select Destination")
        self.dest_selector.clicked.connect(self.select_dest)
        self.source_adder = QPushButton("Add Sources")
        self.source_adder.clicked.connect(self.add_sources)
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.addWidget(self.dest_selector)
        self.buttons_layout.addWidget(self.source_adder)
        self.buttons_widget = QWidget()
        self.buttons_widget.setLayout(self.buttons_layout)
        # Create the filenames layout
        
        self.dest_path = QLineEdit()
        self.dest_path.setReadOnly(True)
        if self.dest_path.text() == "":
            self.dest_path.setPlaceholderText("No destination selected")
        else:
            self.dest_path.setPlaceholderText(self.dest_path.text())
        self.source_list = QListWidget()
        self.filenames_layout = QVBoxLayout()
        self.filenames_layout.addWidget(self.dest_path)
        self.filenames_layout.addWidget(self.source_list)
        self.filenames_widget = QWidget()
        self.filenames_widget.setLayout(self.filenames_layout)
        # Create the main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.buttons_widget)
        self.main_layout.addWidget(self.filenames_widget)
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)
    
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
            self.dest_path.setText(paths[0])
    
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
                if path not in self.sources:
                    self.sources.append(path)
            pass

