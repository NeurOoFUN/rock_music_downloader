import os
import os.path
import re
from typing import Callable

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from database import MusicDbManager
from data_collection import Parser


class Ui_MainWindow(QMainWindow):
    """

    The app.
    """
    def __init__(self):
        super().__init__()

        self.setObjectName("MainWindow")

        self.db_instance = MusicDbManager()
        self.parser = Parser()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.setCentralWidget(self.centralwidget)

        self.vbox = QtWidgets.QVBoxLayout(self.centralwidget)

        self.show_all_groups_button = self.push_button_create(
                'show_all_groups_button', 'Show all groups',
                70, self.show_all_groups_button_slot
                )
        self.show_genres_button = self.push_button_create(
                'show_genres_button', 'Show genres',
                70, self.show_genres_button_slot
                )

        self.log_from_parser_module = self.log_label_create(
                'log_from_parser_module'
                )
        self.log_from_parser_module.hide()
        self.log_from_writer_module = self.log_label_create(
                'log_from_writer_module'
                )
        self.log_from_writer_module.hide()

        self.music_list = self.list_widget_create(
                'music_list', self.db_instance.show_all_groupnames_or_genges('group_name'),
                self.parser_lounch
                )
        self.music_list.hide()
        self.genres_list = self.list_widget_create(
                'genres_list', self.db_instance.show_all_groupnames_or_genges('genre'),
                self.show_music_of_the_particularly_genre
                )
        self.genres_list.hide()

        self.back_button = self.push_button_create(
                'back_button', '<<Back', 13, self.back_from_the_list
                )
        self.back_button.hide()

    def show_music_of_the_particularly_genre(self, item):
        """

        This method is genres_list's slot.
        """
        self.music_by_genre_list = self.list_widget_create(
                'music_by_genre_list',
                self.db_instance.get_groups_of_selected_genre(item.text()),
                self.parser_lounch
                )

        self.back_button.hide()
        self.vbox.addWidget(self.music_by_genre_list)
        self.music_by_genre_list.show()
        self.genres_list.hide()

        self.back_to_genre_button = self.push_button_create(
                'back_to_genre_button', '<<Back to genres',
                13, self.back_to_genre_button_slot
                )
        self.back_to_genre_button.show()

    def parser_lounch(self, item):
        self.music_list.hide()
        self.genres_list.hide()
        self.back_button.hide()
        self.pushButton.hide()

        self.parser.path_for_music = self.file_dialog().strip()

        selected_group = self.db_instance.group_selection(item.text())
        self.parser.link_to_selected_group = selected_group

        filtered_group_name = self.parser.group_name = re.sub(r'[><:"/\|?* ]', '_', item.text())

        if not os.path.exists(item.text()):
            os.mkdir(os.path.normpath(f'{self.parser.path_for_music}/{filtered_group_name}'))


        self.live_albums = self.msg_box_create('Do you need live albums?', self.user_answer)

        self.music_list.hide()

        self.log_from_writer_module.show()
        self.log_from_parser_module.show()

        self.parser.parse(self.log_from_parser_module, self.log_from_writer_module)

        self.log_from_writer_module.hide()
        self.log_from_parser_module.hide()

        self.show_all_groups_button.show()
        self.show_genres_button.show()

    def back_from_the_list(self):
        self.music_list.hide()
        self.genres_list.hide()
        self.back_button.hide()
        self.show_all_groups_button.show()
        self.show_genres_button.show()

    def show_all_groups_button_slot(self):
        self.music_list.show()
        self.show_all_groups_button.hide()
        self.show_genres_button.hide()
        self.music_list.show()
        self.back_button
        self.back_button.show()
       
    def show_genres_button_slot(self):
        self.genres_list.show()
        self.show_genres_button.hide()
        self.show_all_groups_button.hide()
        self.genres_list.show()
        self.back_button
        self.back_button.show()

    def back_to_genre_button_slot(self):
        self.back_to_genre_button.hide()
        self.music_by_genre_list.hide()
        self.back_button.show()
        self.genres_list.show()

    def user_answer(self, button):
        """

        This method is live_albums's slot.
        """
        self.parser.user_answer = button.text()

    def list_widget_create(
            self, objname: str, items: list | set, slot: Callable[[str], None]
            ) -> QtWidgets.QListWidget:
        list_font = QtGui.QFont()
        list_font.setPointSize(15)

        self.list = QtWidgets.QListWidget(self)
        self.list.setObjectName(objname)
        self.list.setFont(list_font)
        self.list.setStyleSheet("color: rgb(0, 170, 0);")
        self.list.addItems(items)
        self.list.itemClicked.connect(slot)

        self.vbox.addWidget(self.list)
        return self.list

    def msg_box_create(self, message: str, slot: Callable[[str], None]):
        msg_box = QMessageBox()
        msg_box.setWindowTitle(' ')
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.addButton(QMessageBox.Yes)
        msg_box.addButton(QMessageBox.No)
        msg_box.buttonClicked.connect(slot)
        msg_box.exec_()

        self.list.hide()

    def log_label_create(self, obj_name: str) -> QtWidgets.QLabel:
        font = QtGui.QFont()
        font.setPointSize(15)
        
        self.log = QtWidgets.QLabel(self)
        self.log.setObjectName(obj_name)
        self.log.setFont(font)
        self.log.setStyleSheet("color: rgb(0, 76, 0);")

        self.vbox.addWidget(self.log)
        return self.log

    def push_button_create(self, obj_name: str, text: str, font_size: int, slot: Callable[[], None]):
        self.pushButton = QtWidgets.QPushButton(self)
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(70)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("color: rgb(0, 170, 0);")
        self.pushButton.setObjectName(obj_name)
        self.pushButton.setText(text)
        self.pushButton.clicked.connect(slot)

        self.vbox.addWidget(self.pushButton)
        return self.pushButton

    def file_dialog(self):
        path_for_music_recording = QtWidgets.QFileDialog.getExistingDirectory()
        return path_for_music_recording

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
