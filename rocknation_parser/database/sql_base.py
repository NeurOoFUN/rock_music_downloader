import sqlite3

class MusicDbManager:
    """
    This class manages database.
    """
    def __init__(self):
        self._connect = sqlite3.connect('database/music.db')
        self._cursor = self._connect.cursor()

    def __del__(self):
        self._connect.commit()
        self._connect.close()

    def create_db(self) -> None:
        create_table = """
            CREATE TABLE IF NOT EXISTS music(
                id INTEGER PRIMARY KEY,
                band_name TEXT,
                band_link TEXT,
                genre TEXT
            )
        """
        self._cursor.execute(create_table)

    def write_all_data_to_db(self, band_name: str, band_link: str, genre: str) -> None:
        self._cursor.execute(
            """INSERT INTO music(band_name, band_link, genre)
               VALUES(?, ?, ?)
            """,
            (band_name, band_link, genre)
            )

    def show_all_bandnames_or_genges(self, value: str) -> list[str] | set[str]:
        all_data = self._cursor.execute(
            f"""SELECT {value} FROM music"""
        ).fetchall()

        names_list = []

        match value:
            case 'band_name':
                names_list = [name for tpl in all_data for name in tpl]
            case 'genre':
                names_list = {name for tpl in all_data for name in tpl}

        return sorted(list(names_list))

    def band_selection(self, choice_of_user: str) -> str:
        user_selected_band = self._cursor.execute(
            """
            SELECT band_link FROM music WHERE band_name = ?
            """,
            (choice_of_user,)
        ).fetchone()
        return user_selected_band[0]

    def get_bands_of_selected_genre(self, *choice_of_user: str) -> list:
        user_selected_band = self._cursor.execute(
                """
                SELECT band_name FROM music WHERE genre = ?
                """,
                (choice_of_user)
                ).fetchall()
        bands_of_chose_genre = [band for i in user_selected_band for band in i]
        return bands_of_chose_genre

