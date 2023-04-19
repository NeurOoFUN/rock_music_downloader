from bs4 import BeautifulSoup

from tools import session
from database.sql_base import MusicDbManager

__all__ = ['find_all_groups']

music_manager_instance = MusicDbManager()


def pagenation_count() -> int:
    response = session.get(url='https://rocknation.su/mp3/').text
    soup = BeautifulSoup(response, 'lxml')
    pagen_link = soup.find('ul', class_='pagination') \
        .find_all('li')[-1].find_all('a')[-1].get('href').split('/')[-1]
    return int(pagen_link) + 1


def find_all_groups() -> None:
    music_manager_instance.create_db()
    for i in range(1, pagenation_count()):
        response = session.get(url='https://rocknation.su/mp3/' + str(i)).text
        soup = BeautifulSoup(response, 'lxml')
        tr_list = soup.find('table', class_='table-bands').find('tbody').find_all('tr')

        for l in tr_list:
            try:
                name = l.find('td').find('a').get_text()
                link = 'https://rocknation.su' + \
                    l.find('td').find('a').get('href')
                genre = l.find_all('td')[1].get_text()

                music_manager_instance.write_all_data_to_db(
                        group_name=name, group_link=link, genre=genre
                        )

            except AttributeError:
                continue

