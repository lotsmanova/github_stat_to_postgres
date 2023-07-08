import psycopg2
import json


class PostgresDB:
    """Класс для взаимодействия с Postgres"""
    def __init__(self, dbname: str, user: str, password: str,
                 host: str = 'localhost', port: str = '5432', table_name: str = 'repos'):
        """Инициализация класса и создание таблицы в БД"""
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()
        self.table_name = table_name

        self._create_table()


    def _create_table(self):
        """Создание таблицы в БД"""
        with self.conn:
            self.cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id SERIAL PRIMARY KEY, 
                name_repos VARCHAR(255), 
                stars INT, 
                forks INT
            );
        """)


    def add_data_to_table(self, stats: list[dict]):
        """Метод добавления данных в таблицу"""
        with self.conn:
            for stat in stats:
                self.cur.execute(
                    f"INSERT INTO {self.table_name} (name_repos, stars, forks) VALUES (%s, %s, %s)",
                    (stat["name"], stat["stars"], stat["forks"]))


    def save_data_to_json(self):
        """Сохранение данных в json и получение данных из таблицы"""
        with self.conn:
            self.cur.execute(f"SELECT * FROM {self.table_name}")
            data = self.cur.fetchall()
            data_dict = [{"id": d[0], "name": d[1], "stars": d[2], "forks": d[3]} for d in data]
            with open(f"{self.table_name}.json", "w") as f:
                json.dump(data_dict, f, indent=4)


    def get_data(self, count: int, sort_by: str = 'name') -> list[dict]:
        """Получение данных из таблицы"""
        with self.conn:
            if sort_by == 'name' or sort_by == 'language':
                self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {sort_by} LIMIT {count}")
            elif sort_by == 'stars' or sort_by == 'forks':
                self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY {sort_by} DESC LIMIT {count}")
            else:
                self.cur.execute(f"SELECT * FROM {self.table_name} ORDER BY name_repos LIMIT {count}")
            data = self.cur.fetchall()
            data_dict = [{"name": d[1], "stars": d[2], "forks": d[3]} for d in data]
            return data_dict