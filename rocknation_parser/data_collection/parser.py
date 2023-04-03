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

        self.link_to_selected_group = str()
        self.user_answer = str()

    def parse(self, log_from_parser_module, log_from_writer_module):
        for self.page_count in range(1, 10):  # pagenation.
            album_number = 1
            response = session.get(
                self.link_to_selected_group + f'/{str(self.page_count)}'
            )

            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips').find('ol', class_='list').find_all('li')

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

                self.album_refs, self.album_name, self.group_name = \
                        self.album_refs, self.album_name, self.group_name

                try:
                    self.download_songs(log_from_writer_module)

                except FileExistsError:
                    print('We have this album, next...')

