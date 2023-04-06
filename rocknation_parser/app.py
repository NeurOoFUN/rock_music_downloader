import os
from typing import Callable

from PyQt5 import QtCore, QtWidgets, QtGui
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
        self.resize(900, 715)

        self.db_instance = MusicDbManager()
        self.parser = Parser()

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 900, 715))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_all_groups = QtWidgets.QWidget()
        self.tab_all_groups.setObjectName("tab_all_groups")
        self.tabWidget.addTab(self.tab_all_groups, "All groups".rjust(129))

        self.tab_all_genres = QtWidgets.QWidget()
        self.tab_all_genres.setObjectName('tab_all_genres')
        self.tabWidget.addTab(self.tab_all_genres, "Genres".rjust(129))


        self.music_list = self.list_widget_create(
                self.tab_all_groups, (0, 0, 900, 690), 'music_list',
                    self.db_instance.show_all_groupnames_or_genges('group_name'), self.parser_lounch
                )

        self.genres_list = self.list_widget_create(
                self.tab_all_genres, (0, 0, 900, 690), 'genres_list',
                    self.db_instance.show_all_groupnames_or_genges('genre'), self.show_music_of_the_particularly_genre
                )
        self.log_from_parser_module = self.log_label_create(
                (10, 450, 881, 121), 'log_from_parser_module'
                )
        self.log_from_writer_module = self.log_label_create(
                (10, 610, 881, 51), 'log_from_writer_module'
                )
        self.completion_notice = self.log_label_create(
                (400, 610, 881, 51), 'completion_notice'
                )

    def show_music_of_the_particularly_genre(self, item):
        """

        This method is genres_list's slot.
        """
        self.music_by_genre_list = self.list_widget_create(
                self.tab_all_genres, (0, 0, 900, 690), 'music_by_genre_list',
                self.db_instance.get_groups_of_selected_genre(item.text()), self.parser_lounch
                )

        self.music_by_genre_list.show()
        self.back_button = self.push_button_create(
                'back_button', '<<Back to genres', self.back_button_signal_handler
                )
        self.back_button.show()

    def parser_lounch(self, item):
        selected_group = self.db_instance.group_selection(item.text())

        if not os.path.exists(item.text()):
            os.mkdir(item.text())

        self.live_albums = self.msg_box_create('Do you need live albums?', self.user_answer)

        self.music_list.hide()
        self.genres_list.hide()
        self.completion_notice.hide()

        self.log_from_writer_module.show()
        self.log_from_parser_module.show()

        self.parser.link_to_selected_group = selected_group
        self.parser.group_name = item.text()
        self.parser.parse(self.log_from_parser_module, self.log_from_writer_module)

        self.log_from_writer_module.hide()
        self.log_from_parser_module.hide()
        self.completion_notice.setText(f'"{item.text()}" downloaded.')

        self.music_list.show()
        self.genres_list.show()
        self.completion_notice.show()

    def back_button_signal_handler(self):
        self.music_by_genre_list.hide()
        self.back_button.hide()

    def user_answer(self, button):
        """

        This method is live_albums's slot.
        """
        self.parser.user_answer = button.text()

    def list_widget_create(
            self, tab: QtWidgets.QTabWidget, geometry: tuple, objname: str, items: list | set, slot: Callable[[str], None]
            ) -> QtWidgets.QListWidget:
        list_font = QtGui.QFont()
        list_font.setPointSize(13)

        self.list = QtWidgets.QListWidget(tab)
        self.list.setGeometry(QtCore.QRect(*geometry))
        self.list.setObjectName(objname)
        self.list.setFont(list_font)
        self.list.addItems(items)
        self.list.itemClicked.connect(slot)
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

    def log_label_create(self, geomettry: tuple, obj_name: str) -> QtWidgets.QLabel:
        font = QtGui.QFont()
        font.setPointSize(30)
        
        self.log = QtWidgets.QLabel(self)
        self.log.setGeometry(QtCore.QRect(*geomettry))
        self.log.setObjectName(obj_name)
        self.log.setFont(font)
        self.log.setStyleSheet("color: rgb(0, 76, 0);")
        return self.log

    def push_button_create(self, obj_name: str, text: str, slot: Callable[[], None]):
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(660, 610, 191, 71))
        self.pushButton.setStyleSheet("color: rgb(0, 255, 0);")
        self.pushButton.setObjectName(obj_name)
        self.pushButton.setText(text)
        self.pushButton.clicked.connect(slot)
        return self.pushButton



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
