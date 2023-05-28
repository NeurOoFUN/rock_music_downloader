import re

from bs4 import BeautifulSoup
from PyQt5 import QtWidgets

from tools import session
from .writer import Saver


__all__ = ['Parser']


class Parser(Saver):
    '''

    This class parses music.
    '''
    def __init__(self):
        super().__init__()

        self.link_to_selected_band = str()
        self.user_answer = str()

    def parse(self, log_from_parser_module: QtWidgets.QLabel,
              log_from_writer_module: QtWidgets.QLabel, 
              step_for_albumpb: QtWidgets.QProgressBar,
              step_for_songpb: QtWidgets.QProgressBar) -> None:

        for self.page_count in range(1, 10):  # pagenation.
            album_number = 1
            response = session.get(
                self.link_to_selected_band + f'/{str(self.page_count)}'
            )

            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips').find('ol', class_='list').find_all('li')
            try:
                step = 100 / len(album_data)
            except ZeroDivisionError:
                return

            for li in album_data:
                self.album_refs = 'http://rocknation.su' + li.find('a').get('href')
                self.album_name = li.get_text()

                if self.user_answer == '&No' and re.search(r'(?i)\blive\b', self.album_name):
                    continue

                log_from_parser_module.setText(
                    f'Page: {self.page_count}, ' +
                    f'Album: {album_number} / {len(album_data)}'
                )

                QtWidgets.QApplication.processEvents()

                album_number += 1

                try:
                    self.download_songs(log_from_writer_module, step_for_songpb)
                    step_for_albumpb.setProperty("value", step)
                    step += 100 / len(album_data)

                except FileExistsError:
                    log_from_writer_module.setText('We have this album, next...')
                    step_for_albumpb.setProperty("value", step)
                    step += 100 / len(album_data)

