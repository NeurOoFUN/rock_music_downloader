import os
import re

from PyQt5 import QtWidgets

from tools import session


class Saver:
    def __init__(self):
        self.album_refs = str()
        self.album_name = str()
        self.group_name = str()

    def download_songs(self, log_from_writer_module):
        """
        Download and save all albums with .mp3 songs.
        """
        response = session.get(url=self.album_refs).text
        # path of downloaded music
        os.mkdir(os.path.normpath(f'{self.group_name}/{self.album_name}'))
        # regex, parse links from JS.
        pattern_of_ref = re.findall(
            r'http://rocknation\.su/upload/mp3/.+?\.mp3',
            response
        )
        song_count = 1
        # download songs.
        for i in pattern_of_ref:
            download = session.get(url=i).content
            # Get the name of the song from song link.
            pattern_of_name = re.findall(r'\d\.(.+)\.mp3', i)[0]
            # Cleaning the name of the song.
            song_name = re.sub(r'[\d %]', r'', pattern_of_name)

            self.music_recording(download, song_count, pattern_of_ref, song_name, log_from_writer_module)

            song_count += 1

    def music_recording(self, download, song_count, pattern_of_ref, song_name, log_from_writer_module) -> None:
            music_path = os.path.normcase(
                f'{self.group_name}/{self.album_name}/{song_count}. {song_name}.mp3'
            )
            # with open(music_path, 'wb') as file:
                # file.write(download)

            log_from_writer_module.setText(f'Song: {song_name} {song_count} / {len(pattern_of_ref)}')

            QtWidgets.QApplication.processEvents()

