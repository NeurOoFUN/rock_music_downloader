import os

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

        music_list_font = QtGui.QFont()
        music_list_font.setPointSize(15)

        self.music_list = QtWidgets.QListWidget(self)
        self.music_list.setGeometry(QtCore.QRect(0, 0, 900, 715))
        self.music_list.setObjectName("music_list")
        self.music_list.setFont(music_list_font)
        self.music_list.addItems(self.db_instance.show_all_groupnames())
        self.music_list.itemClicked.connect(self.parser_lounch)

        self.log_from_parser_module = self.log_label((10, 450, 881, 121), 'log_from_parser_module')
        self.log_from_writer_module = self.log_label((10, 610, 881, 51), 'log_from_writer_module')
        self.completion_notice = self.log_label((400, 610, 881, 51), 'completion_notice')

    def parser_lounch(self, item):
        selected_group = self.db_instance.group_selection(item.text())

        if not os.path.exists(item.text()):
            os.mkdir(item.text())

        msg_box = QMessageBox()
        msg_box.setWindowTitle(' ')
        msg_box.setText('Do you need live albums?')
        msg_box.setIcon(QMessageBox.Information)
        msg_box.addButton(QMessageBox.Yes)
        msg_box.addButton(QMessageBox.No)
        msg_box.buttonClicked.connect(self.user_answer)
        msg_box.exec_()

        self.music_list.hide()
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
        self.completion_notice.show()

    def user_answer(self, button):
        self.parser.user_answer = button.text()

    def log_label(self, geomettry: tuple, obj_name: str):
        font = QtGui.QFont()
        font.setPointSize(30)
        
        self.log = QtWidgets.QLabel(self)
        self.log.setGeometry(QtCore.QRect(*geomettry))
        self.log.setObjectName(obj_name)
        self.log.setFont(font)
        self.log.setStyleSheet("color: rgb(0, 76, 0);")
        return self.log



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    main_window = Ui_MainWindow()

    main_window.show()

    sys.exit(app.exec_())
